import { ButtonHTMLAttributes } from "react";

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  loading?: boolean;
}

export const Button = ({ loading, children, ...props }: Props) => {
  return (
    <button
      {...props}
      disabled={loading || props.disabled}
      style={{
        padding: "10px 16px",
        background: "#111",
        color: "#fff",
        border: "none",
        cursor: "pointer",
      }}
    >
      {loading ? "Processing..." : children}
    </button>
  );
};
