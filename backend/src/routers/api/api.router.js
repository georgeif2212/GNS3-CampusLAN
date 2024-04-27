import { Router } from "express";

const router = Router();

router.get("/data", (req, res) => {
  res.json({ message: "Hello from Express!" });
});
  

router.get("/products", (req, res) => {
  const products = [
    { id: 1, name: "Product 1" },
    { id: 2, name: "Product 2" },
    { id: 3, name: "Product 3" },
  ];

  res.status(200).json({ products });
});

export default router;
