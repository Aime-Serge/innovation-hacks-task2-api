import express, { Express, Request, Response } from "express";
import { errorHandler } from "./middleware/errorHandler";
import { notFoundHandler } from "./middleware/notFoundHandler";

export function createApp(): Express {
  const app = express();

  app.use(express.json());

  app.get("/health", (_req: Request, res: Response) => {
    res.status(200).json({ status: "ok" });
  });

  // Resource routers are mounted here (added in subsequent commits).

  app.use(notFoundHandler);
  app.use(errorHandler);

  return app;
}
