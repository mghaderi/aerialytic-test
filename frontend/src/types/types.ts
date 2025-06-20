// Represents the output of solar panel angle calculations for all three models
export interface CalculationResult {
    pvlib: {
        optimal_pitch: number; // Optimal tilt angle in degrees (0–90)
        optimal_azimuth: number; // Optimal azimuth angle in degrees (0–360)
    };
    nrel: {
        optimal_pitch: number;
        optimal_azimuth: number;
    };
    liu_jordan: {
        optimal_pitch: number;
        optimal_azimuth: number;
    };
}
