import React from "react";
import { VolumeViewer } from "./VolumeViewer";

/**
 * App
 */
export const App: React.FC = () => {
  return (
    <div style={{width: "100%", height: "100vh", backgroundColor: "#cccccc"}}>
      <VolumeViewer />
    </div>
  );
};
