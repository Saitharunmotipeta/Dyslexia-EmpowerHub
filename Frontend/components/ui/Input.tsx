import { InputHTMLAttributes } from "react";

export const Input = (props: InputHTMLAttributes<HTMLInputElement>) => {
  return (
    <input
      {...props}
      style={{
        padding: "10px",
        border: "1px solid #ccc",
        marginBottom: "12px",
        width: "100%",
      }}
    />
  );
};
