import React, { useState } from 'react';
import { 
  TextField, 
  Button, 
  Stack, 
  Alert, 
  CircularProgress,
  InputAdornment,
  Box
} from '@mui/material';
import { 
  Search as SearchIcon
} from '@mui/icons-material';
import { personService } from '../../services/api';
import { Person } from '../../types/persons';
import { AuthUtils } from '../../config/auth';

interface RutSearchFormProps {
  onPersonFound: (person: Person) => void;
  onError: (error: string) => void;
}

// Validación de RUT chileno
const validateRut = (rut: string): boolean => {
  return AuthUtils.validateRUT(rut);
};

// Formato de RUT
const formatRut = (rut: string): string => {
  return AuthUtils.formatRUT(rut);
};

const RutSearchForm: React.FC<RutSearchFormProps> = ({ onPersonFound, onError }) => {
  const [rut, setRut] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formattedRut, setFormattedRut] = useState('');

  const handleRutChange = (value: string) => {
    const cleanValue = value.replace(/[^0-9kK]/g, '');
    setRut(cleanValue);
    setFormattedRut(formatRut(cleanValue));
    setError(null);
  };

  const handleSubmit = async (e?: React.FormEvent) => {
    if (e) {
      e.preventDefault();
    }
    
    if (!rut.trim()) {
      setError('Por favor ingrese un RUT');
      return;
    }

    if (!validateRut(rut)) {
      setError('RUT inválido');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const response = await personService.searchPersonByRut(formattedRut);
      onPersonFound(response);
    } catch (err: any) {
      const errorMessage = err.response?.status === 404 
        ? 'Persona no encontrada' 
        : err.response?.status === 422 
        ? 'RUT inválido' 
        : 'Error en la búsqueda';
      setError(errorMessage);
      onError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Stack spacing={3}>
        <Stack direction="row" spacing={2} alignItems="center">
          <TextField
            value={formattedRut}
            onChange={(e) => handleRutChange(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="12.345.678-9"
            disabled={loading}
            autoFocus
            size="small"
            fullWidth
            error={!!error}
            sx={{
              '& .MuiOutlinedInput-root': {
                backgroundColor: 'rgba(30, 41, 59, 0.8)',
                color: '#f8fafc',
                '& fieldset': {
                  borderColor: error ? '#f87171' : '#475569',
                },
                '&:hover fieldset': {
                  borderColor: error ? '#f87171' : '#3b82f6',
                },
                '&.Mui-focused fieldset': {
                  borderColor: error ? '#f87171' : '#3b82f6',
                },
              },
              '& .MuiInputBase-input': {
                color: '#f8fafc',
              },
              '& .MuiInputBase-input::placeholder': {
                color: '#94a3b8',
              },
            }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon sx={{ color: '#94a3b8' }} />
                </InputAdornment>
              ),
            }}
          />
          <Button
            type="submit"
            variant="contained"
            disabled={loading || !rut.trim()}
            startIcon={loading ? <CircularProgress size={16} /> : <SearchIcon />}
            sx={{
              minWidth: 120,
              height: 40,
              background: loading ? '#475569' : 'linear-gradient(135deg, #3b82f6, #06b6d4)',
              '&:hover': {
                background: loading ? '#475569' : 'linear-gradient(135deg, #2563eb, #0891b2)',
              },
              '&:disabled': {
                background: '#475569',
                color: '#94a3b8',
              },
            }}
          >
            {loading ? 'Buscando...' : 'Buscar'}
          </Button>
        </Stack>
        
        {error && (
          <Alert severity="error" sx={{ mt: 1 }}>
            {error}
          </Alert>
        )}
      </Stack>
    </Box>
  );
};

export default RutSearchForm;
