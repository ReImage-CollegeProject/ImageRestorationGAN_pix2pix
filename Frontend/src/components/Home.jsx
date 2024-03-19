import "./home.css";
import { useState, useEffect } from "react";
function Home() {
  const images = ["test1.jpeg", "test2.jpeg", "test3.jpeg"];

  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  useEffect(() => {
    const slideshowInterval = setInterval(() => {
      setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 3000);

    return () => clearInterval(slideshowInterval);
  }, [images.length]);
  return (
    <div id="landing-div">
      <div id="content">
        <div id="inner">
          <span>Image Enchancement</span>
          <h1>Art of Restoration</h1>
          <h1>ReImage</h1>
          <p>
            Presenting you Image restoration tools empowered by neural network,
          </p>
          <p>Transforming Images, One Click at a Time</p>
          <p>with ease of use</p>
        </div>
        <div id="image-container">
          {images.map((image, index) => (
            <img
              key={index}
              src={image}
              alt={`Image ${index + 1}`}
              style={{
                opacity: index === currentImageIndex ? 1 : 0,
                transition: "opacity 1s ease-in-out",
                position: "absolute",
              }}
            />
          ))}
        </div>
      </div>
      <div id="footer">
        <a href="#about-dev">About Developer</a>
        <a href="#aboutreimage">About ReImage</a>
        <a href="#message_part">leave message</a>
      </div>
      <hr />
      <div id="about-dev">
        <h2>Meet our Developers</h2>
        <div id="content">
          <img src="/saurab.jpg" alt="" />
          <div id="inner">
            <p>
              As the Machine Learning Developer behind ReImage, I specialize in
              PyTorch, Computer Vision, and have a particular focus on
              implementing advanced models like Conditional Variational
              Autoencoders (CVAE). My work revolves around pushing the
              boundaries of image enhancement technology, with a recent emphasis
              on optimizing the CVAE model for real-time, high-quality image
              enhancement. In the development of ReImage, I spearheaded the
              creation of a robust CVAE model, leveraging the capabilities of
              PyTorch to achieve remarkable results in improving image clarity,
              details, and overall visual appeal. Overcoming various challenges,
              the model has been fine-tuned to meet the specific requirements of
              ReImage, providing users with unparalleled image enhancement
              capabilities.Feel free to connect with me through my social media
              links below
            </p>

            <a
              href="https://linkedin.com/in/sujan"
              target="_blank"
              rel="noopener noreferrer"
            >
              <i
                class="fa-brands fa-linkedin-in"
                style={{ color: "#ffffff" }}
              ></i>
            </a>
            <a
              href="https://github.com/saurabtharu/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <i
                className="fab fa-github fa-lg"
                style={{ color: "#ffffff" }}
              ></i>
            </a>
          </div>
        </div>
        <div id="content">
          <img src="/sujan.jpeg" alt="" />
          <div id="inner">
            <p>
              Hello! I'm Sujan, the developer behind ReImage. I'm passionate
              about creating engaging and user-friendly applications. With a
              focus on front-end technologies like React, I strive to deliver
              seamless and enjoyable experiences for users. In addition to
              coding, I love exploring new technologies, solving problems, and
              continuously enhancing my skills. When it comes to machine
              learning, I specialize in testing models and creating efficient
              data loaders. I enjoy the challenge of optimizing algorithms and
              ensuring they perform well in various scenarios. Whether it's
              fine-tuning hyperparameters or preprocessing data, I'm dedicated
              to delivering robust and reliable machine learning solutions. Feel
              free to connect with me through my social media links below:
            </p>
            <a
              href="https://linkedin.com/in/sujan"
              target="_blank"
              rel="noopener noreferrer"
            >
              <i
                class="fa-brands fa-linkedin-in"
                style={{ color: "#ffffff" }}
              ></i>
            </a>
            <a
              href="https://github.com/sujankdk-10"
              target="_blank"
              rel="noopener noreferrer"
            >
              <i
                className="fab fa-github fa-lg"
                style={{ color: "#ffffff" }}
              ></i>
            </a>
          </div>
        </div>

        <div id="content">
          <img src="/subash.jpeg" alt="" />
          <div id="inner">
            <p>
              Hi there! I'm Subash, the backend developer for ReImage. My focus
              is on crafting robust and efficient server-side solutions using
              Django. I have a passion for building scalable APIs and optimizing
              database performance to ensure a smooth user experience. In
              addition to backend development, I play a crucial role in the
              training part of our model. I delve into coding, implementing
              algorithms, and fine-tuning models to achieve the best results for
              ReImage. I believe in the power of machine learning to transform
              user experiences and am dedicated to pushing the boundaries of
              what's possible. Connect with me through the following links:
            </p>
            <a
              href="https://www.linkedin.com/in/subash-tamang-458b6123a/"
              target="_blank"
            >
              <i
                class="fa-brands fa-linkedin-in lg"
                style={{ color: "#ffffff" }}
              ></i>
            </a>
            <a href="https://github.com/Nihanglama" target="_blank">
              <i
                className="fab fa-github fa-lg"
                style={{ color: "#ffffff" }}
              ></i>
            </a>
          </div>
        </div>
      </div>
      <hr />
      <div id="aboutreimage">
        <h2>About ReImage</h2>
        <p>
          With the increasing number of digital devices, the number of people
          capturing photos has increased. This has led to demand for utility
          tools that can remove some level of degradation from images and
          provide noise free, unblurred images. We have utilized the power of
          deep learning techniques called Variational Autoencoders(VAEs) to
          build a tool which deals with degraded images. Our project "ReImage"
          attempts to remove blurriness, noise and scratches from images that
          might have occurred due to compression, distortion in image due to
          digital inference, and also while being captured because of extremely
          high or low light exposure, misfocus of camera. The model has been
          trained on a large dataset of high-quality images, which have enabled
          it to capture the underlying pattern of images. Because of this
          capturing ability, the model can generate new, noise-free images from
          degraded inputs. Our VAE-based restoration technique outperforms
          traditional methods, and it doesn't even require a clean version of
          the image for an unseen image as a reference. Our tool enhances the
          visual perception, which improves the accuracy in medical imaging,
          enables better decision-making in autonomous driving and contributes
          to the development of computer vision applications. It can even be
          used to preserve historical images by restoring them to their original
          quality.
        </p>
      </div>
      <hr />
      <div id="message_part">
        <h2>Leave a Message</h2>
        <div className="leave-message-container">
          <h2>MessageBox</h2>
          <form className="message-form">
            <input type="text" placeholder="Enter your name" />
            <textarea
              placeholder="Type your message here..."
              rows="4"
              cols="50"
            />
            <br />
            <button type="submit">Submit</button>
          </form>
        </div>
      </div>
    </div>
  );
}
export default Home;
