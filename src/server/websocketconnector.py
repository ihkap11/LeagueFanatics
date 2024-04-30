from loguru import logger
from typing import Dict
from fastapi import WebSocket
from starlette.websockets import WebSocketState
from uuid import UUID
import json


class WebSocketConnectionManager:
    """
    Full Duplex WebSocket
    - maintain list of active connections
    - connect
    - disconnect
    - disconnect_all
    - send message
    - broadcast
    """

    def __init__(
        self,
        active_connections: Dict[str, WebSocket] = None,
        # asyncio.Lock
    ) -> None:
        """Initializes WebSocketConnectionManager with an optional dictionary of active connections.

        Args:
            active_connections (Dict[str, WebSocket], optional): Dictionary of active connections. Defaults to None.
        """

        if active_connections is None:
            active_connections = {}

        self.active_connections: Dict[str, WebSocket] = active_connections

    async def connect(self, websocket: WebSocket, client_id: str) -> None:
        """
        Accepts new client connection and appends it to the dictionary of active connections.

        Args:
            websocket (WebSocket): WebSocket instance representing client connection.
            client_id (str): Unique identifier of the client.
        """
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(
            f"[NEW CONNECTION] {client_id} \n[TOTAL] {len(self.active_connections)}"
        )

    async def disconnect(self, client_id: str) -> None:
        """Disconnects websocket by removing from dictionary of active connections.

        Args:
            websocket (WebSocket): WebSocket instance representing client connection.
        """
        try:
            if client_id in self.active_connections:
                websocket = self.active_connections[client_id]
                if websocket.application_state != WebSocketState.DISCONNECTED:
                    await websocket.close()
                logger.info(
                    f"[CONNECTION DISCONNECTED] {client_id} \n[TOTAL] {len(self.active_connections)}"
                )
            del self.active_connections[client_id]
        except ValueError:
            logger.warn("WebSocket connection not found.")

    async def disconnect_all(self) -> None:
        """Reset active connections."""
        self.active_connections = []

    async def send_message(self, message: Dict, client_id: str) -> None:
        """Send personal message to target client.

        Args:
            message (Dict): JSON serializable dictionary containing the message to send.
            client_id (str): WebSocket instance representing client connection.
        """
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            if websocket.application_state == WebSocketState.CONNECTED:
                await websocket.send_text(message)
            else:
                logger.error(
                    f"Attempt to send a message on a closed connection for client {client_id}"
                )

    async def broadcast(self, message: Dict) -> None:
        """Broadcast message to all clients.

        Args:
            message (Dict): JSON serializable dictionary containing the message to send.
        """
        for _, websocket in self.active_connections.items():
            await self.send_message(message, websocket)
