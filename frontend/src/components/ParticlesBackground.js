import React from "react";
import Particles from "react-tsparticles";

const ParticlesBackground = () => (
  <Particles
    options={{
      fpsLimit: 60,
      interactivity: { events: { onClick: { enable: true, mode: "push" } } },
      particles: { number: { value: 50 }, size: { value: 3 } },
    }}
  />
);

export default ParticlesBackground;
