interface Props {
    title: string;
    pitch: number;
    azimuth: number;
}

// Displays a single solar angle result block (e.g., for Pvlib, NREL, or Liu-Jordan)
const Calculator: React.FC<Props> = ({ title, pitch, azimuth }) => (
    <div className="results-container">
        <h2>{title}</h2>
        <p><strong>Optimal Pitch (Tilt):</strong> {pitch.toFixed(2)}°</p>
        <p><strong>Optimal Azimuth:</strong> {azimuth.toFixed(2)}°</p>
    </div>
);

export default Calculator;
