import { CalculationResult } from '../types/types';
import Calculator from './Calculator';

// Displays the results from each solar angle model (Pvlib, NREL, Liu-Jordan)
const Calculators: React.FC<{ result: CalculationResult }> = ({ result }) => (
    <>
        <Calculator
            title="Pvlib"
            pitch={result.pvlib.optimal_pitch}
            azimuth={result.pvlib.optimal_azimuth}
        />
        <Calculator
            title="NREL"
            pitch={result.nrel.optimal_pitch}
            azimuth={result.nrel.optimal_azimuth}
        />
        <Calculator
            title="Liu Jordan"
            pitch={result.liu_jordan.optimal_pitch}
            azimuth={result.liu_jordan.optimal_azimuth}
        />
    </>
);

export default Calculators;
