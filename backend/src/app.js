import express from "express";
import next from "next";
import config from "./config/config.js";

import apiRouter from "./routers/api/api.router.js";

const dev = config.env;
const app = express();
const nextApp = next({ dev }); // Crea la aplicación Next.js
const handle = nextApp.getRequestHandler(); // Obtiene el manejador de Next.js

app.use(express.json()); 
app.use(express.urlencoded({ extended: true }));

// Prepara Next.js y luego inicializa tus rutas y middleware personalizados
nextApp.prepare().then(() => {

  app.get("/",(req,res)=>{
    res.redirect("/home")
  })

  app.get("/home", (req, res) => {
    return nextApp.render(req, res, "/home"); 
  });

  app.get("/products", (req, res) => {
    return nextApp.render(req, res, "/products"); 
  });

  app.use("/api", apiRouter);

  // * Maneja las demás rutas con Next
  app.all("*", (req, res) => {
    return handle(req, res);
  });
});

export default app;
