#!/bin/bash

# 定义镜像名称和标签
IMAGE_TAG="latest"
CONTAINER_NAME=""

# 定义旧容器名称和新容器名称
while [[ $# -gt 0 ]]; do
    case "$1" in
        -n|--name)
            CONTAINER_NAME="$2"
            shift
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [-n|--name] container_name"
            exit 1
            ;;
    esac
done

# 检查容器名称是否为空
if [[ -z $CONTAINER_NAME ]]; then
    echo "容器名称不能为空。"
    echo "Usage: $0 [-n|--name] container_name"
    exit 1
fi

# 1. 备份容器的端口映射、目录挂载和环境变量
OLD_PORT_MAPPINGS=$(docker inspect -f '{{range $p, $conf := .NetworkSettings.Ports}}~{{$p}}{{$conf}} {{end}}' $XIAOYA_NAME | tr '~' '\n' | tr '/' ' ' | tr -d '[]{}' | awk '{printf("-p %s:%s\n",$3,$1)}' | grep -Eo "\-p [0-9]{1,10}:[0-9]{1,10}" | tr '\n' ' ')
OLD_VOLUME_MAPPINGS=$(docker inspect --format='{{range $v,$conf := .Mounts}} -v {{$conf.Source}}:{{$conf.Destination}} {{$conf.Type}}~{{end}}' $CONTAINER_NAME | tr '~' '\n' | grep bind | sed 's/bind//g' | grep -Eo "\-v .*:.*" | tr '\n' ' ')
OLD_ENV_VARS=$(docker inspect -f '{{range $e, $v := .Config.Env}}{{$v}} {{end}}' $CONTAINER_NAME 2>/dev/null | sed '/^$/d' | tr '~' '\n' | sed '/^$/d' | awk '{printf("-e \\\"%s\\\"\n",$0)}' | tr '\n' ' ')
IMAGE_NAME=$(docker inspect -f '{{.Config.Image}}' $CONTAINER_NAME |sed 's/:.*//')

# 2. 停止并删除旧容器
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME

# 3. 拉取最新的镜像
docker pull $IMAGE_NAME:$IMAGE_TAG

echo "docker run -d --name $CONTAINER_NAME $OLD_PORT_MAPPINGS  $OLD_VOLUME_MAPPINGS  $IMAGE_NAME:$IMAGE_TAG"

# 4. 创建新容器，并应用备份的端口映射、目录挂载和环境变量
docker run -d \
    --name $CONTAINER_NAME \
    $OLD_PORT_MAPPINGS \    # 应用备份的端口映射
    $OLD_VOLUME_MAPPINGS \  # 应用备份的目录挂载
#    $OLD_ENV_VARS \         # 应用备份的环境变量
    $IMAGE_NAME:$IMAGE_TAG


# 5. (可选) 等待一段时间，确保新容器正常启动
sleep 5

# 6. (可选) 查看新容器的运行状态
docker ps | grep $CONTAINER_NAME