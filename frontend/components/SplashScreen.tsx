"use client";

import { useEffect, useState } from "react";

export default function SplashScreen() {
  const [visible, setVisible] = useState(true);
  const [exiting, setExiting] = useState(false);

  useEffect(() => {
    const exitTimer = setTimeout(() => {
      setExiting(true);
    }, 2300);

    const hideTimer = setTimeout(() => {
      setVisible(false);
    }, 2900);

    return () => {
      clearTimeout(exitTimer);
      clearTimeout(hideTimer);
    };
  }, []);

  if (!visible) return null;

  return (
    <div
      className={`splash-screen ${
        exiting ? "splash-screen-exit" : ""
      }`}
    >
      <div className="splash-grid" />

      <div className="splash-content">
        <div className="logo-container">
          <img
            src="/mean-media-logo.png"
            alt="Mean Media"
            className="splash-logo"
          />
        </div>

        <div className="splash-brand">
          MEAN MEDIA AI
        </div>

        <div className="splash-status">
          <span className="status-dot" />
          INITIALIZING INTELLIGENCE ENGINE
        </div>

        <div className="splash-loader">
          <div className="splash-loader-bar" />
        </div>
      </div>

      <div className="splash-corner splash-corner-tl">
        MM / 001
      </div>

      <div className="splash-corner splash-corner-tr">
        SYSTEM ONLINE
      </div>

      <div className="splash-corner splash-corner-bl">
        SEO + GEO INTELLIGENCE
      </div>

      <div className="splash-corner splash-corner-br">
        V.01
      </div>
    </div>
  );
}