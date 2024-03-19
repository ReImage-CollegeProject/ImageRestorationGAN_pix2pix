import React, { useState } from "react";
import axios from "axios";
import "./download.css";
import { useLocation } from "react-router-dom";

function Download() {
  const [loading, setLoading] = useState(false);
  const [img, setImg] = useState(null);
  const location = useLocation();
  const id = location.state?.id;
  const image = location.state?.image;
  const [error ,setError]=useState("")

  let imageUrl = "";

  if (typeof image === "object" && image instanceof File) {
    imageUrl = URL.createObjectURL(image);
  } else if (typeof image === "string") {
    imageUrl = image;
  }
  console.log(id);
  console.log(image);

  const fetchImages = async () => {
    console.log("clicked");
    try {
      setLoading(true);
      const token = localStorage.getItem("token");
      const response = await axios.get(`/api/convert_image/${id}`, {
        headers: {
          Authorization: "Token " + token,
        },
      });
      setImg(response.data.image);
      console.log("no errors")
    } catch (error) {
      console.log("got error")
      setError(error.response.data.error_messages)
    } finally {
      setLoading(false);
    }
  };
  const Download = () => {
    const link = document.createElement("a");
    link.href = img; // Assuming img is the URL of the converted image
    link.download = "downloaded_image.jpg"; // You can set the desired file name
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <>
      <div className="downloads">
        {!loading && (
          <div id="image">
            <img src={imageUrl} alt="" />
          </div>
        )}
        {img && !loading && (
          <div id="image">
            <img src={img} alt="converted image" />
          </div>
        )}

        {loading && (
          <div id="animation">
            <div id="water" className="drop"></div>
            <p>Denoising your image .....</p>
            <div id="water" className="wave"></div>
          </div>
        )}
      </div>
      <div id="mybtns">
        <button onClick={fetchImages}>Denoise Image</button>
        <button onClick={Download}>Download Image</button>
        {error && <p style={{ color: "red" }}>{error}</p>}
      </div>
    </>
  );
}

export default Download;
