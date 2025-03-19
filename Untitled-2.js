import React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";

export default function Home() {
  return (
    <div className="relative min-h-screen bg-black text-white scroll-smooth overflow-hidden">
      <BackgroundAnimation />

      <section className="relative z-10 flex flex-col-reverse lg:flex-row items-center justify-between max-w-7xl mx-auto px-6 pt-24 pb-16">
        <motion.div
          className="w-full lg:w-1/2 text-center lg:text-left"
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 1 }}
        >
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold leading-tight mb-6">
            Unleash the Power of <br />Transforming Manual Processes
          </h1>
          <p className="text-gray-400 text-lg mb-6">
            At AutomataX, we believe automation is the key to unlocking efficiency, reducing cost, and driving sustainable growth through smart technology.
          </p>
          <Button className="text-lg px-6 py-3 rounded-2xl bg-white text-black hover:bg-gray-200 transition">Get Started</Button>
        </motion.div>

        <motion.div
          className="w-full lg:w-1/2 flex justify-center mb-12 lg:mb-0"
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 1 }}
        >
          <img src="/robot-image.png" alt="Futuristic Robot" className="w-full max-w-md lg:max-w-xl" />
        </motion.div>
      </section>

      <div className="absolute top-0 left-0 w-full h-full z-0">
        <BackgroundAnimation />
      </div>
    </div>
  );
}

function BackgroundAnimation() {
  return (
    <div className="absolute inset-0 -z-10">
      <svg className="w-full h-full" preserveAspectRatio="xMidYMid slice">
        <defs>
          <radialGradient id="grad" cx="50%" cy="50%" r="100%">
            <stop offset="0%" stopColor="#ffffff22" />
            <stop offset="100%" stopColor="#000000" />
          </radialGradient>
        </defs>
        <rect width="100%" height="100%" fill="url(#grad)" />
        <circle cx="50%" cy="50%" r="0.5" fill="#ffffff33">
          <animate attributeName="r" values="0.5;200;0.5" dur="20s" repeatCount="indefinite" />
        </circle>
      </svg>
    </div>
  );
}
