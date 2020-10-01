from fastapi import APIRouter

from api.api_v1.endpoints import user,country,channel,shop,shop_executor,channel_manager,sim,login,shop_sim,url

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["user"])
api_router.include_router(country.router, prefix="/country", tags=["country"])
api_router.include_router(channel.router, prefix="/channel", tags=["channel"])
api_router.include_router(shop.router, prefix="/shop", tags=["shop"])
api_router.include_router(shop_executor.router, prefix="/shop-executor", tags=["shop-executor"])
api_router.include_router(shop_sim.router, prefix="/shop-sim", tags=["shop-sim"])
api_router.include_router(channel_manager.router, prefix="/channel_manager", tags=["channel-manager"])
api_router.include_router(sim.router, prefix="/sim", tags=["sim"])
api_router.include_router(url.router, prefix="/url", tags=["url"])
