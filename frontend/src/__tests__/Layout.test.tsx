import { render, screen } from '@testing-library/react';
import Layout from '../layouts/Index';

test('renders children inside layout', () => {
    render(<Layout><p>Test Content</p></Layout>);
    expect(screen.getByText(/Test Content/)).toBeInTheDocument();
});
