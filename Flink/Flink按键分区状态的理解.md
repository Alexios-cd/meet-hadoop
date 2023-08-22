# 综述
FLink中算子任务可以分为**无状态**和**有状态** 两种情况，在有状态下出现了状态的分类。  
Flink 的状态有两种：托管状态（Managed State）和原始状态（Raw State）。托管状态就是由 Flink
统一管理的，状态的存储访问、故障恢复和重组等一系列问题都由 Flink 实现，我们只要调接口就可以；
而原始状态则是自定义的，相当于就是开辟了一块内存，需要我们自己管理，实现状态的序列化和故
障恢复。  
其中状态细分如下：  

![img.png](images/EE6B372C599841919F639474AEDAF1A9.png)
## 两种托管状态
![img.png](images/C4853CB2CDA04CD38641EDAA776F04FF.png)
![img_1.png](images/1046DDF2B4E5417CBE0FE0732464DD72.png)
### 按键分区状态
其中按键分区状态（Keyed State）是我们常用的操作，需要注意，使用 Keyed State 必须基于 KeyedStream。没有进行 keyBy 分区的 DataStream，即使转
换算子实现了对应的富函数类，也不能通过运行时上下文访问 Keyed State。

总结如下：
1. 经过keyBy之后进入按键分区状态，相同的key会进入相同的分区状态处理逻辑（对应的算子）。但是同一个分区状态对应的算子可能有多个不同的key会进入。
2. 只能保障相同的key进入相同的按键分区状态，但是保障同一个按键分区状态只有一个key会进入。
 
eg1：6个不同的key在算子 2个并行度情况下，同一个按键分区状态会进入3个不同的key
eg2：6个不同的key在算子 1个并行度情况下，同一个按键分区状态会进入6个不同的key
eg3：6个不同的key在算子 6个并行度情况下，同一个按键分区状态只会进入1个不同的key
同一个按键分区状态保障了相同的key不会乱跑，但是由于资源有限可能会重复利用部分空间，具体需要看key的数据量和并行度。

部分数据流如下：
![img.png](images/85D9CED1B2534DE497D0564D96B0B81E.png)
验证代码如下：
```java
package com.xxxxxxx.study.key;

import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.api.common.typeinfo.TypeHint;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.datastream.DataStreamSource;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import java.util.HashSet;

/**
 * 描述：TODO 写明类的作用
 * <p>
 * 作者： 
 * <p>
 * 结论：
 * 1. 经过keyBy之后进入按键分区状态，相同的key会进入相同的分区状态处理逻辑（对应的算子）。但是同一个分区状态对应的算子可能有多个不同的key会进入。
 * 只能保障相同的key进入相同的按键分区状态，但是保障同一个按键分区状态只有一个key会进入，eg：6个不同的key在算子 2个并行度情况下，每个算子会进入3个不同的key
 * 日期： 2023/8/22 9:39
 */
public class KeyStateDemo {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(2);
        String dataStr = "aThis bdocumentation ais bfor can cout-of-date cversiona dof dApache aFlink bWe arecommend byou ause bthe alatest bstable aversion";
        DataStreamSource<String> dataStreamSource = env.fromElements(dataStr.split(" "));
        SingleOutputStreamOperator<String> result = dataStreamSource.keyBy(el -> el.toLowerCase().charAt(0)).map(new ChartMapFunction());
        result.print();
        env.execute("KeyStateDemo");

    }

    public static class ChartMapFunction extends RichMapFunction<String, String> {

        private ValueState<HashSet<String>> state;

        @Override
        public void open(Configuration parameters) throws Exception {
            ValueStateDescriptor<HashSet<String>> valueState = new ValueStateDescriptor<>("hashSet-container", TypeInformation.of(new TypeHint<HashSet<String>>() {
            }));
            state = getRuntimeContext().getState(valueState);
            System.out.println("初始化成功…………" + getRuntimeContext().getIndexOfThisSubtask() + "state对象为：" + state);

        }

        @Override
        public String map(String value) throws Exception {
            // System.out.println("中间结果:" +getRuntimeContext().getTaskNameWithSubtasks()+ value);
            System.out.println(getRuntimeContext().getIndexOfThisSubtask()+"开始处理："+value);
            HashSet<String> map = state.value();
            if (map == null) {
                map = new HashSet<>();
            }
            if (map.contains(value)) {
                return "需要过滤：" + value;
            } else {
                map.add(value);
                state.update(map);
                return value;
            }
        }


    }
}

```
输出如下：
```shell
初始化成功…………1state对象为：org.apache.flink.runtime.state.heap.HeapValueState@771c49a9
初始化成功…………0state对象为：org.apache.flink.runtime.state.heap.HeapValueState@669cb44b
1开始处理：aThis
0开始处理：bdocumentation
2> aThis
1开始处理：ais
1> bdocumentation
2> ais
0开始处理：bfor
1开始处理：dof
2> dof
1> bfor
1开始处理：dApache
0开始处理：can
2> dApache
1开始处理：aFlink
2> aFlink
1> can
1开始处理：arecommend
2> arecommend
1开始处理：ause
2> ause
1开始处理：alatest
0开始处理：cout-of-date
2> alatest
1开始处理：aversion
2> aversion
1> cout-of-date
0开始处理：cversiona
1> cversiona
0开始处理：bWe
1> bWe
0开始处理：byou
1> byou
0开始处理：bthe
1> bthe
0开始处理：bstable
1> bstable
```
同时建议将 按键分区 状态定义在open当中，定义在外部 没有实际意义 ，因为在内部获取时依然是两个不同的按键分区状态：
eg：
```java
package com.xxxxxx.study.key;

import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.api.common.typeinfo.TypeHint;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.datastream.DataStreamSource;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import java.util.HashSet;

/**
 * 描述：TODO 写明类的作用
 * <p>
 * 作者：
 * <p>
 * 结论：
 * 1. 经过keyBy之后进入按键分区状态，相同的key会进入相同的分区状态处理逻辑（对应的算子）。但是同一个分区状态对应的算子可能有多个不同的key会进入。
 * 只能保障相同的key进入相同的按键分区状态，但是保障同一个按键分区状态只有一个key会进入，eg：6个不同的key在算子 2个并行度情况下，每个算子会进入3个不同的key
 * 日期： 2023/8/22 9:39
 */
public class KeyStateDemo2 {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(2);
        String dataStr = "aThis bdocumentation ais bfor can cout-of-date cversiona dof dApache aFlink bWe arecommend byou ause bthe alatest bstable aversion";
        DataStreamSource<String> dataStreamSource = env.fromElements(dataStr.split(" "));



        ValueStateDescriptor<HashSet<String>> valueState = new ValueStateDescriptor<>("hashSet-container", TypeInformation.of(new TypeHint<HashSet<String>>() {
        }));
        SingleOutputStreamOperator<String> result = dataStreamSource.keyBy(el -> el.toLowerCase().charAt(0)).map(new ChartMapFunction(valueState));
        result.print();
        env.execute("KeyStateDemo");

    }

    public static class ChartMapFunction extends RichMapFunction<String, String> {

        private final ValueStateDescriptor<HashSet<String>> valueState1;
        private ValueState<HashSet<String>> state;

        public ChartMapFunction(ValueStateDescriptor<HashSet<String>> valueState) {
            valueState1 = valueState;
        }

        @Override
        public void open(Configuration parameters) throws Exception {
            state = getRuntimeContext().getState(valueState1);
            System.out.println("初始化成功…………" + getRuntimeContext().getIndexOfThisSubtask() + "state对象为：" + state);

        }

        @Override
        public String map(String value) throws Exception {
            System.out.println("使用state" + getRuntimeContext().getIndexOfThisSubtask() + "state对象为：" + state);
            return value;
        }


    }
}
```
输出如下：
```shell
初始化成功…………1state对象为：org.apache.flink.runtime.state.heap.HeapValueState@1dcf1b6c
初始化成功…………0state对象为：org.apache.flink.runtime.state.heap.HeapValueState@59d7b2d2
使用state1state对象为：org.apache.flink.runtime.state.heap.HeapValueState@1dcf1b6c
使用state0state对象为：org.apache.flink.runtime.state.heap.HeapValueState@59d7b2d2
2> aThis
使用state1state对象为：org.apache.flink.runtime.state.heap.HeapValueState@1dcf1b6c
2> ais
使用state1state对象为：org.apache.flink.runtime.state.heap.HeapValueState@1dcf1b6c
2> dof
使用state1state对象为：org.apache.flink.runtime.state.heap.HeapValueState@1dcf1b6c
2> dApache
使用state1state对象为：org.apache.flink.runtime.state.heap.HeapValueState@1dcf1b6c
2> aFlink
1> bdocumentation
使用state1state对象为：org.apache.flink.runtime.state.heap.HeapValueState@1dcf1b6c
2> arecommend
使用state1state对象为：org.apache.flink.runtime.state.heap.HeapValueState@1dcf1b6c
2> ause
使用state1state对象为：org.apache.flink.runtime.state.heap.HeapValueState@1dcf1b6c
2> alatest
使用state0state对象为：org.apache.flink.runtime.state.heap.HeapValueState@59d7b2d2
1> bfor
使用state0state对象为：org.apache.flink.runtime.state.heap.HeapValueState@59d7b2d2
1> can
使用state1state对象为：org.apache.flink.runtime.state.heap.HeapValueState@1dcf1b6c
使用state0state对象为：org.apache.flink.runtime.state.heap.HeapValueState@59d7b2d2
1> cout-of-date
2> aversion
使用state0state对象为：org.apache.flink.runtime.state.heap.HeapValueState@59d7b2d2
1> cversiona
使用state0state对象为：org.apache.flink.runtime.state.heap.HeapValueState@59d7b2d2
1> bWe
使用state0state对象为：org.apache.flink.runtime.state.heap.HeapValueState@59d7b2d2
1> byou
使用state0state对象为：org.apache.flink.runtime.state.heap.HeapValueState@59d7b2d2
1> bthe
使用state0state对象为：org.apache.flink.runtime.state.heap.HeapValueState@59d7b2d2
1> bstable
```
较为规范的应该如下：
```java
package com.xxxxxx.study.key;

import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.api.common.typeinfo.TypeHint;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.datastream.DataStreamSource;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import java.util.HashSet;

/**
 * 描述：TODO 写明类的作用
 * <p>
 * 作者：
 * <p>
 * 结论：
 * 1. 经过keyBy之后进入按键分区状态，相同的key会进入相同的分区状态处理逻辑（对应的算子）。但是同一个分区状态对应的算子可能有多个不同的key会进入。
 * 只能保障相同的key进入相同的按键分区状态，但是保障同一个按键分区状态只有一个key会进入，eg：6个不同的key在算子 2个并行度情况下，每个算子会进入3个不同的key
 * 日期： 2023/8/22 9:39
 */
public class KeyStateDemo2 {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(2);
        String dataStr = "aThis bdocumentation ais bfor can cout-of-date cversiona dof dApache aFlink bWe arecommend byou ause bthe alatest bstable aversion";
        DataStreamSource<String> dataStreamSource = env.fromElements(dataStr.split(" "));
        ValueStateDescriptor<HashSet<String>> valueState = new ValueStateDescriptor<>("hashSet-container", TypeInformation.of(new TypeHint<HashSet<String>>() {
        }));
        SingleOutputStreamOperator<String> result = dataStreamSource.keyBy(el -> el.toLowerCase().charAt(0)).map(new ChartMapFunction());
        result.print();
        env.execute("KeyStateDemo");

    }

    public static class ChartMapFunction extends RichMapFunction<String, String> {

        private ValueState<HashSet<String>> state;

        @Override
        public void open(Configuration parameters) throws Exception {
            ValueStateDescriptor<HashSet<String>> valueState = new ValueStateDescriptor<>("hashSet-container", TypeInformation.of(new TypeHint<HashSet<String>>() {
            }));
            state = getRuntimeContext().getState(valueState);
            System.out.println("初始化成功…………" + getRuntimeContext().getIndexOfThisSubtask() + "state对象为：" + state);

        }

        @Override
        public String map(String value) throws Exception {
            System.out.println("使用state" + getRuntimeContext().getIndexOfThisSubtask() + "state对象为：" + state);
            return value;
        }


    }
}

```

