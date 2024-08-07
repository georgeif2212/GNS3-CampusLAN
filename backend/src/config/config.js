import dotenv from "dotenv";

dotenv.config();
export default {
  port: process.env.PORT || 8080,
  env: process.env.NODE_ENV || "production",
};
