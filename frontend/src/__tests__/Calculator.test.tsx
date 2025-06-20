import { render, screen } from '@testing-library/react';
import Calculator from '../components/Calculator';

test('renders pitch and azimuth correctly', () => {
    render(<Calculator title="Test" pitch={45.1234} azimuth={180.5678} />);
    expect(screen.getByText(/Test/i)).toBeInTheDocument();
    expect(screen.getByText(/45.12°/)).toBeInTheDocument();
    expect(screen.getByText(/180.57°/)).toBeInTheDocument();
});
