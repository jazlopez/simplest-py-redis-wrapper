# simplest-py-redis-wrapper


Simple implementation of py-redis that allows to create, list and invalidate redis cache items.

#### BEFORE GET STARTED

Provide host and password to your redis instance. If your connection does not require password either unset the
environment variable REDIS_AUTH_PASSWORD or set it to empty string.

```yaml
# Define your connection user password and host to connect to 
export REDIS_AUTH_PASSWORD=YourRedisInstancePassword
export REDIS_HOST_URI=ENDPOINT_URL_OR_IP_ADDRESS

# more customization available
# export REDIS_PORT=6379
# export REDIS_ENCODING=utf-8
# export REDIS_TIMEOUT=10
```

#### USAGE

Available commands

* Seed (create) cache items

```shell
# Create 50 cache items. If -n is not provided defaults to 10 items
python main.py seed -n 50
```

* List cache items
```shell

python main.py list

```

* Invalidate cache

```shell

python main.py flush

```

#### VERSION

0.0.0 Initial

#### CONTRIBUTIONS

All welcome. Open a pull request with fixes and enhacements.

#### CONTACT

[Jaziel Lopez Software Engineer](jazlopez@github.com)
