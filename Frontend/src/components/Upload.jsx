import React, { useState } from "react";
import axios from "axios";
import "./upload.css";
import Download from "./Download";
import { Link, useNavigate } from "react-router-dom";

const Upload = () => {
  const [image, setImage] = useState(null);
  const [name, setName] = useState("");
  const [status, setStatus] = useState(false);
  const [error, setError] = useState("");
  const [uploading, setUploading] = useState(false);
  const [id, setId] = useState("");
  const navigate = useNavigate();

  const token = localStorage.getItem("token");

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  const handleImageChange = (e) => {
    const selectedImage = e.target.files[0];
    setImage(selectedImage);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedImage = e.dataTransfer.files[0];
    setImage(droppedImage);
  };

  const handleClick = () => {
    setImage(null);
    setStatus(false);
    setError("");
  };

  const handleUpload = async () => {
    if (!image) {
      setError("Please select a PNG image");
      return;
    }
    if (!name.trim()) {
      setError("Name is required");
      return;
    }

    try {
      setUploading(true);

      const formData = new FormData();
      formData.append("image", image);
      formData.append("name", name);

      const response = await axios.post("/api/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: "Token " + token,
        },
      });

      console.log("Upload success:", response.data.id);
      setId(response.data.id);
      setStatus(true);
      setName("");
      setError("");
    } catch (error) {
      if (error.response) {
        setError(
          `You are not authorized. ${error.response.status} ${error.response.statusText}`
        );
      } else if (error.request) {
        setError(error.request);
      } else {
        setError(error.message);
      }
    } finally {
      setUploading(false);
    }
  };

  return (
    <div id="image-handle">
      <div className="image-handle">
        <div id="change-img">
          {image && <img src={URL.createObjectURL(image)} alt="Selected" />}
          <label
            htmlFor="upload-input"
            className="custom-file-upload"
            onDragOver={handleDragOver}
            onDrop={handleDrop}
          >
            <i className="fa-regular fa-images fa-2xl"></i>
            Drop image or click to upload
          </label>
          <input
            type="file"
            accept="image/"
            id="upload-input"
            onClick={handleClick}
            onChange={handleImageChange}
            style={{ display: "none" }}
          />
        </div>
        <input
          type="text"
          name="name"
          placeholder="Name of image"
          value={name}
          onChange={handleNameChange}
        />
        <button onClick={handleUpload} disabled={uploading}>
          {uploading ? "Uploading..." : "Upload Image"}
        </button>
        {error && <p id="uploading">{error}</p>}
      </div>
      {status && navigate('/denoise', { state: { id ,image} })}
    </div>
  );
};

export default Upload;
