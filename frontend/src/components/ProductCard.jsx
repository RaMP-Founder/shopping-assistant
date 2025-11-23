import React from "react";

export default function ProductCard({ product, premium=false }){
  const imageUrl = product.image_path && (product.image_path.startsWith("http") ? product.image_path : `http://localhost:8000/product_images/${product.image_path}`);
  return (
    <div className={`product-premium ${premium ? "" : ""}`}>
      <img src={imageUrl} alt={product.name} className="w-20 h-20 object-contain rounded-md" />
      <div className="flex-1">
        <div className="text-sm font-semibold text-white">{product.name}</div>
        <div className="text-xs text-gray-300 mt-1">{product.subtitle}</div>
        <div className="mt-3 flex items-center justify-between">
          <a href={product.url} target="_blank" rel="noreferrer" className="btn-gold px-3 py-1 text-sm">Buy Now</a>
          <div className="text-sm text-gray-300">{product.price ? `₹${product.price}` : ""}</div>
        </div>
      </div>
    </div>
  );
}
