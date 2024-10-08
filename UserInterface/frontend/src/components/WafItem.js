import React from "react";

const WafItem = ({ item, editItem, handleDelete }) => (
  <li
    key={item.id}
    className="list-group-item d-flex justify-content-between align-items-center"
  >
    <span className="waf-title mr-2" title={item.description}>
      {item.name}
    </span>
    <span>
      <button
        className="btn btn-secondary mr-2"
        onClick={() => editItem(item)}
      >
        Edit
      </button>
      <button
        className="btn btn-danger"
        onClick={() => handleDelete(item)}
      >
        Delete
      </button>
    </span>
  </li>
);

export default WafItem;