import uuid
import os


def module_not_found_exit(module_name=None, exit_code=1):
    """
    :param module_name:
    :param exit_code:
    :return:
    """
    print(f"[ERROR] {module_name} missing, run: pip install {module_name}")
    exit(exit_code)


REDIS_AUTH_PASSWORD = os.getenv(key="REDIS_AUTH_PASSWORD", default=None)
REDIS_HOST_URI = os.getenv(key="REDIS_HOST_URI", default=None)
REDIS_PORT = os.getenv(key="REDIS_PORT", default=6379)
REDIS_ENCODING = os.getenv(key="REDIS_ENCODING", default="utf-8")
REDIS_TIMEOUT = os.getenv(key="REDIS_TIMEOUT", default=10)
# -----------------------------------------
# non builtin python modules required block
# -----------------------------------------
try:
    import redis
except ImportError:
    module_not_found_exit(module_name="redis")
try:
    import click
except ImportError:
    module_not_found_exit(module_name="click")
try:
    from faker import Faker
except ImportError:
    module_not_found_exit(module_name="faker")

if not REDIS_HOST_URI:
    click.secho(f"ERROR {__file__} could not be executed. Environment variable name: REDIS_HOST_URI is missing.",
                fg="red")
    exit(1)

if not REDIS_AUTH_PASSWORD:
    click.secho(f"[WARNING]: Did you forget to provide a password to your redis connection?", fg="yellow")

@click.group("cli")
@click.pass_context
def cli(ctx):

    ctx.obj = {}
    click.secho(f"[INFO] Attempting to connect to {REDIS_HOST_URI}")

    try:

        if REDIS_AUTH_PASSWORD:

            client = redis.Redis(socket_connect_timeout=REDIS_TIMEOUT,  socket_timeout=REDIS_TIMEOUT, ssl=True,
                             password=REDIS_AUTH_PASSWORD, host=REDIS_HOST_URI, decode_responses=True,
                             encoding=REDIS_ENCODING, port=REDIS_PORT)
        else:

            client = redis.Redis(socket_connect_timeout=REDIS_TIMEOUT,  socket_timeout=REDIS_TIMEOUT,
                                 host=REDIS_HOST_URI, decode_responses=True,
                                 encoding=REDIS_ENCODING, port=REDIS_PORT)

        client.ping()
        ctx.obj["client"] = client

    except Exception as e:
        click.secho(f"[ERROR] {e}", fg="red")
        exit(1)


@cli.command("seed")
@click.pass_context
@click.option("--number", "-n", required=True, type=int)
def _seed_(ctx, number):
    """
    :param ctx:
    :param number:
    :return:
    """

    faker = Faker()
    client = ctx.obj["client"]

    try:
        click.secho("=============================================================================", fg="blue")
        click.secho(f"\t\tProvision {number} elements in cache cluster", fg="blue")
        click.secho("=============================================================================", fg="blue")
        i = 0
        while i < number:
            key = str(uuid.uuid4())
            data = dict({"name": str(faker.name()), "address": str(faker.address()).replace("\n", " ")})
            click.secho(data, fg="blue")
            client.set(key, str(data))
            i = i+1
    except Exception as e:
        click.secho(f"[ERROR] {e}", fg="red")
        exit(1)


@cli.command("list")
@click.pass_context
def _list_(ctx):

    """

    :param ctx:
    :return:
    """
    client = ctx.obj["client"]
    for i, key in enumerate(client.keys()):
        try:
            click.secho(f"{i+1}\tKey={key}\t{client.get(key)}", fg="blue")
        except Exception as e:
            print(e)
            continue

@cli.command("flush")
@click.pass_context
def _flush_(ctx):
    client = ctx.obj["client"]
    client.flushall()


if __name__ == "__main__":
    cli()
