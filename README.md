# Kubernetes-кластер (minikube)

Демонстрационный Kubernetes-кластер с приложением на Python (Flask) и Helm-чартом

## Подготовка

### Запуск локального кластера Minikube

```bash
minikube start
```

### Включение Ingress-контроллера

```bash
minikube addons enable ingress
kubectl get pods -n ingress-nginx
```

---

## Сборка Docker-образа приложения

### Настройка Docker на использование среды Minikube

```bash
eval $(minikube docker-env)
```

### Сборка Flask-приложения

```bash
docker build -t server-app ./docker
```

---

## Развертывание приложения

### Применение Kubernetes-манифестов

```bash
kubectl apply -f manifests/
```

### Проверка состояния компонентов

```bash
kubectl get pods           # Список всех подов
kubectl get svc            # Список всех сервисов
kubectl get ingress        # Список всех ingress-ресурсов
```

---

## Доступ к приложению

### Получение URL через NodePort

```bash
minikube service app-service --url
curl http://<выданный-адрес>
```

### Настройка доступа через Ingress

Добавьте запись в `/etc/hosts`:

```bash
<minikube-ip> app.local
```

Проверка доступа:

```bash
curl http://app.local
```

---

## Масштабирование приложения

### Увеличение количества реплик

```bash
kubectl scale deployment app --replicas=3
kubectl get pods
```

---

### Запуск Minikube с двумя узлами

```bash
minikube start --nodes 2
kubectl get nodes
```

---

## Установка Helm-приложения `echo-server`

### Добавление и обновление репозитория Helm

```bash
helm repo add ealenn https://ealenn.github.io/charts
helm repo update
```

### Установка Helm-чарта

```bash
helm upgrade -i echo-server ealenn/echo-server \
  -f echo-server/echo-values.yaml \
  --namespace default \
  --create-namespace \
  --force
```

### Добавление в hosts

```bash
echo "$(minikube ip) echo.minikube.local" | sudo tee -a /etc/hosts
```

### Проверка установки

```bash
kubectl get pods
kubectl get ingress
curl http://echo.minikube.local
curl http://echo.minikube.local/?echo_body=HelloWorld
```

---

## Helm-чарт echo-app

### Удаление и повторная установка

```bash
helm uninstall echo-app
helm install echo-app ./echo-app --set replicaCount=1 -f ./echo-app/values.yaml
```

### Мониторинг подов и проверка сервиса

```bash
kubectl get pods -w
curl $(minikube service echo-app-service --url)
```

### Масштабирование

```bash
kubectl scale deployment echo-app --replicas=3
for i in {1..10}; do
  curl -s $(minikube service echo-app-service --url)
done
```

---