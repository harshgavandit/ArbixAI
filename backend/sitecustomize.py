import warnings

# sitecustomize is imported early on Python startup (when cwd is on sys.path).
# Suppress DeprecationWarning about asyncio.iscoroutinefunction originating
# from third-party libraries (Starlette / FastAPI) on Python 3.14+.
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=r".*asyncio.iscoroutinefunction.*",
)
