import reflex as rx

config = rx.Config(
    app_name="example",
    db_url="sqlite:///pynecone.db",
    env=rx.Env.DEV,
    frontend_packages=[],
)
