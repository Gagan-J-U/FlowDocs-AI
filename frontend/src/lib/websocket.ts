export type WebSocketMessage =
  | { type: "message"; data: any }
  | { type: "typing"; user_id: string; thread_id: string }
  | { type: "online_status"; user_id: string; online: boolean }
  | { type: "message_read"; message_id: string }
  | { type: "message_delivered"; message_id: string };

export class WebSocketService {

  private ws: WebSocket | null = null;

  private url: string;

  private reconnectAttempts = 0;

  private maxReconnectAttempts = 5;

  private reconnectDelay = 3000;

  private handlers: Map<string, Function[]> =
    new Map();

  private isConnecting = false;

  constructor(
    websocketUrl: string
  ) {

    this.url = websocketUrl;
  }

  connect(): Promise<void> {

    return new Promise(

      (
        resolve,
        reject
      ) => {

        if (
          this.isConnecting
        ) {

          reject(
            new Error(
              "Already connecting"
            )
          );

          return;
        }

        this.isConnecting = true;

        try {

          this.ws = new WebSocket(
            this.url
          );

          this.ws.onopen = () => {

            console.log(
              "WebSocket connected:",
              this.url
            );

            this.isConnecting =
              false;

            this.reconnectAttempts =
              0;

            this.emit(
              "connected"
            );

            resolve();
          };

          this.ws.onmessage = (
            event
          ) => {
            console.log(
              "RAW WEBSOCKET:",
              event.data
            );
            try {

              const message =
                JSON.parse(
                  event.data
                );

              console.log(
                "RAW WS MESSAGE:",
                message
              );

              this.emit(
                "message",
                message
              );

            } catch (error) {

              console.error(
                "Failed to parse websocket message:",
                error
              );
            }
          };

          this.ws.onerror = (
            error
          ) => {

            console.error(
              "WebSocket error:",
              error
            );

            this.isConnecting =
              false;

            reject(error);
          };

          this.ws.onclose = () => {

            console.log(
              "WebSocket disconnected"
            );

            this.isConnecting =
              false;

            this.emit(
              "disconnected"
            );

            this.attemptReconnect();
          };
        }

        catch (error) {

          this.isConnecting =
            false;

          reject(error);
        }
      }
    );
  }

  send(
    content: string
  ) {

    if (
      !this.ws ||
      this.ws.readyState !==
      WebSocket.OPEN
    ) {

      console.error(
        "WebSocket not connected"
      );

      return;
    }

    this.ws.send(

      JSON.stringify({

        content
      })
    );
  }

  private attemptReconnect() {

    if (
      this.reconnectAttempts >=
      this.maxReconnectAttempts
    ) {

      console.error(
        "Max reconnect attempts reached"
      );

      return;
    }

    this.reconnectAttempts++;

    const delay =

      this.reconnectDelay *

      Math.pow(
        2,
        this.reconnectAttempts - 1
      );

    console.log(

      `Reconnecting in ${delay}ms`
    );

    setTimeout(() => {

      this.connect().catch(
        console.error
      );

    }, delay);
  }

  on(
    event: string,
    handler: Function
  ) {

    if (
      !this.handlers.has(
        event
      )
    ) {

      this.handlers.set(
        event,
        []
      );
    }

    this.handlers
      .get(event)!
      .push(handler);

    return () => {

      const handlers =
        this.handlers.get(
          event
        );

      if (!handlers)
        return;

      const index =
        handlers.indexOf(
          handler
        );

      if (index > -1) {

        handlers.splice(
          index,
          1
        );
      }
    };
  }

  private emit(
    event: string,
    data?: any
  ) {

    const handlers =

      this.handlers.get(
        event
      ) || [];

    handlers.forEach(
      (handler) =>
        handler(data)
    );
  }

  disconnect() {

    this.maxReconnectAttempts =
      0;

    if (this.ws) {

      this.ws.close();

      this.ws = null;
    }
  }

  isConnected(): boolean {

    return (
      this.ws?.readyState ===
      WebSocket.OPEN
    );
  }
}

export function createWebSocketService(
  websocketUrl: string
) {

  return new WebSocketService(
    websocketUrl
  );
}