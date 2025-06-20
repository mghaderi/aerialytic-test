import { render, screen } from '@testing-library/react';
import MapComponent from '../components/Map';

describe('MapComponent', () => {
    const props = {
        center: { lat: 43.65, lng: -79.38 },
        marker: { lat: 43.65, lng: -79.38 },
        onClick: jest.fn(),
        apiKey: 'test-key',
    };

    it('renders map container when apiKey is present', () => {
        render(<MapComponent {...props} />);
        expect(screen.getByTestId('map-container')).toBeInTheDocument();
    });
    
    it('shows error message when apiKey is missing', () => {
        render(<MapComponent {...props} apiKey={undefined} />);
        expect(screen.getByText(/Google Maps API key not found/i)).toBeInTheDocument();
    });
});
