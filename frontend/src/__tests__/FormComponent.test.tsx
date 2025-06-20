import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import FormComponent from '../components/Form';
import React from 'react';

describe('FormComponent', () => {
    const mockProps = {
        latitude: '43.65',
        longitude: '-79.38',
        setLatitude: jest.fn(),
        setLongitude: jest.fn(),
        onResult: jest.fn(),
        onError: jest.fn(),
        setLoading: jest.fn(),
        setMapPosition: jest.fn(),
    };

    it('renders input fields and button', () => {
        render(<FormComponent {...mockProps} />);
        expect(screen.getByLabelText(/Latitude/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Longitude/i)).toBeInTheDocument();
        expect(screen.getByLabelText('Offset Angle (optional):')).toBeInTheDocument();
        expect(screen.getByText(/Calculate Optimal Angles/i)).toBeInTheDocument();
    });

    it('shows error on invalid latitude', async () => {
        render(<FormComponent {...mockProps} latitude="999" />);
        fireEvent.click(screen.getByText(/Calculate Optimal Angles/i));
        await waitFor(() => {
            expect(mockProps.onError).toHaveBeenCalledWith('Please enter valid latitude (-90 to 90)');
        });
    });

    it('shows error on invalid longitude', async () => {
        render(<FormComponent {...mockProps} longitude="999" />);
        fireEvent.click(screen.getByText(/Calculate Optimal Angles/i));
        await waitFor(() => {
            expect(mockProps.onError).toHaveBeenCalledWith('Please enter valid longitude (-180 to 180)');
        });
    });

    it('shows error on invalid offset', async () => {
        render(<FormComponent {...mockProps} />);
        fireEvent.change(screen.getByLabelText(/Offset Angle/i), { target: { value: '100' } });
        fireEvent.click(screen.getByText(/Calculate Optimal Angles/i));
        await waitFor(() => {
            expect(mockProps.onError).toHaveBeenCalledWith('Please enter valid Offset Angle (0 to 90)');
        });
    });
});
