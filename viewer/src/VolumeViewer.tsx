import React, { useEffect, useRef, useState } from "react";
import "@kitware/vtk.js/favicon";
import "@kitware/vtk.js/Rendering/Profiles/Volume";

import vtkFullScreenRenderWindow from "@kitware/vtk.js/Rendering/Misc/FullScreenRenderWindow";
import vtkVolume from "@kitware/vtk.js/Rendering/Core/Volume";
import vtkVolumeMapper from "@kitware/vtk.js/Rendering/Core/VolumeMapper";
import vtkVolumeProperty from "@kitware/vtk.js/Rendering/Core/VolumeProperty";
import vtkColorTransferFunction from "@kitware/vtk.js/Rendering/Core/ColorTransferFunction";
import vtkPiecewiseFunction from "@kitware/vtk.js/Common/DataModel/PiecewiseFunction";
import vtkXMLImageDataReader from "@kitware/vtk.js/IO/XML/XMLImageDataReader";

/**
 * VolumeViewer
 */
export const VolumeViewer: React.FC = () => {
    const containerRef = useRef<HTMLDivElement>(null);
    const [fileData, setFileData] = useState<ArrayBuffer | null>(null);

    useEffect(() => {
        if (!fileData || !containerRef.current) return;

        // full screen render window
        const fullScreenRenderWindow = vtkFullScreenRenderWindow.newInstance({
            container: containerRef.current,
            background: [0.1, 0.1, 0.3],  // background color of window
        });
        const renderer = fullScreenRenderWindow.getRenderer();
        const renderWindow = fullScreenRenderWindow.getRenderWindow();

        // reading .vti
        const reader = vtkXMLImageDataReader.newInstance();
        reader.parseAsArrayBuffer(fileData);

        // volume mapper
        const volumeMapper = vtkVolumeMapper.newInstance();
        volumeMapper.setInputConnection(reader.getOutputPort());

        // color
        const colorFunc = vtkColorTransferFunction.newInstance();
        colorFunc.addRGBPoint(0, 0.0, 0.0, 0.0);      // black
        colorFunc.addRGBPoint(128, 1.0, 1.0, 1.0);    // white

        // opcaity
        const opacityFunc = vtkPiecewiseFunction.newInstance();
        opacityFunc.addPoint(0, 0.0);   // transparent
        opacityFunc.addPoint(128, 1.0); // non-transparent

        // volume property
        const volumeProperty = vtkVolumeProperty.newInstance();
        volumeProperty.setRGBTransferFunction(0, colorFunc);
        volumeProperty.setScalarOpacity(0, opacityFunc);
        volumeProperty.setInterpolationTypeToLinear();
        volumeProperty.setShade(true);

        // volume actor
        const volume = vtkVolume.newInstance();
        volume.setMapper(volumeMapper);
        volume.setProperty(volumeProperty);

        renderer.addVolume(volume);
        renderer.resetCamera();
        renderWindow.render();

        // cleanup
        return () => { 
            fullScreenRenderWindow.delete()
        };
    }, [fileData]);

    /**
     * file attach handler
     */
    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) { return; }
        const reader = new FileReader();
        reader.onload = () => setFileData(reader.result as ArrayBuffer);
        reader.readAsArrayBuffer(file);
    };

    /**
     * GUI
     */
    return (
        <div>
            {/* file attach */}
            <input type="file" accept=".vti" onChange={handleFileUpload} />

            {/* container of vtk.js canvas */}
            <div
                ref={containerRef}
                style={{ width: "800px", height: "640px", border: "1px solid black" }}
            />
        </div>
    );
};
