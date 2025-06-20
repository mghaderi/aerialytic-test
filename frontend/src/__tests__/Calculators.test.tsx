import { render, screen } from '@testing-library/react';
import Calculators from '../components/Calculators';
import { CalculationResult } from '../types/types';

const mockResult: CalculationResult = {
    pvlib: { optimal_pitch: 40, optimal_azimuth: 180 },
    nrel: { optimal_pitch: 42, optimal_azimuth: 170 },
    liu_jordan: { optimal_pitch: 45, optimal_azimuth: 160 },
};

test('renders calculators for all three models', () => {
    render(<Calculators result={mockResult} />);
    expect(screen.getByText(/Pvlib/)).toBeInTheDocument();
    expect(screen.getByText(/NREL/)).toBeInTheDocument();
    expect(screen.getByText(/Liu Jordan/)).toBeInTheDocument();
});
