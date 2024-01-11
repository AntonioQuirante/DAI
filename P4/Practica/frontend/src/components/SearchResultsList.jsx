import React from "react";
import "./SearchResultsList.css";
import { SearchResult } from "./SearchResult";

export const SearchResultsList = ({ results }) => {
  const renderCardRows = () => {
    return results.map((result, id) => (
      <div key={id} className="col-md-4">
        <div className="card">
          <div className="card-body">
            <h5 className="card-title">{result.title}</h5>
            <h5 className="card-title">{result.price}€</h5>
            <h5 className="card-title">{result.description}</h5>
          </div>
        </div>
      </div>
    ));
  };

  return (
    <div className="row card-container">
      {renderCardRows()}
    </div>
  );
};
