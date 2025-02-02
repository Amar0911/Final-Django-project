// document.addEventListener("DOMContentLoaded", () => {
//     const modals = document.querySelectorAll(".modal");
//     modals.forEach((modal) => {
//       modal.addEventListener("hidden.bs.modal", (event) => {
//         const video = modal.querySelector("video");
//         if (video) {
//           video.pause(); 
//           video.currentTime = 0; 
//         }
//       });
//     });
//   });


// document.addEventListener("DOMContentLoaded", function () {
//   const playBtn = document.querySelector("#playBtn");
//   const videoContainer = document.querySelector("#videoContainer");
//   const videoPlayer = document.querySelector("#videoPlayer");

//   if (playBtn && videoContainer) {
//       playBtn.addEventListener("click", function () {
//           videoContainer.style.display = "block"; 

//           if (videoPlayer) {
//               videoPlayer.play().catch(error => {
//                   console.error("Autoplay prevented:", error);
//               });
//           }
//       });

//       window.addEventListener("beforeunload", function () {
//           if (videoPlayer) {
//               videoPlayer.pause();
//               videoPlayer.currentTime = 0;
//           }
//       });
//   } else {
//       console.error("Play button or video container not found!");
//   }
// });
