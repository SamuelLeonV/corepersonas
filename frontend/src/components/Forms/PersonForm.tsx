import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Typography,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  CardActions,
  Divider,
  Chip,
  InputAdornment,
  SelectChangeEvent,
  Stack,
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Person,
  PersonForm as PersonFormType,
  RELIGION_OPTIONS,
  RutValidation,
} from '../../types/persons';
import {
  Person as PersonIcon,
  Email as EmailIcon,
  Phone as PhoneIcon,
  LocationOn as LocationOnIcon,
  CalendarToday as CalendarTodayIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
} from '@mui/icons-material';

import { AuthUtils } from '../../config/auth';

// Validación de RUT chileno
const validateRut = (rut: string): boolean => {
  return AuthUtils.validateRUT(rut);
};

// Formato de RUT
const formatRut = (rut: string): string => {
  return AuthUtils.formatRUT(rut);
};

// Esquema de validación
const validationSchema = yup.object().shape({
  rut: yup
    .string()
    .required('El RUT es obligatorio')
    .min(8, 'El RUT debe tener al menos 8 caracteres')
    .max(12, 'El RUT no puede tener más de 12 caracteres')
    .test('rut-valid', 'RUT inválido', (value) => {
      return value ? validateRut(value) : false;
    }),
  nombre: yup
    .string()
    .required('El nombre es obligatorio')
    .min(1, 'El nombre debe tener al menos 1 carácter')
    .max(100, 'El nombre no puede tener más de 100 caracteres'),
  apellido: yup
    .string()
    .required('El apellido es obligatorio')
    .min(1, 'El apellido debe tener al menos 1 carácter')
    .max(100, 'El apellido no puede tener más de 100 caracteres'),
  religion: yup
    .string()
    .required('La religión es obligatoria')
    .min(1, 'La religión debe tener al menos 1 carácter')
    .max(50, 'La religión no puede tener más de 50 caracteres'),
  email: yup
    .string()
    .email('Email inválido')
    .nullable()
    .default(null),
  telefono: yup
    .string()
    .matches(/^[+]?[\d\s\-\(\)]*$/, 'Teléfono inválido')
    .nullable()
    .default(null),
  direccion: yup
    .string()
    .max(200, 'La dirección no puede tener más de 200 caracteres')
    .nullable()
    .default(null),
  fecha_nacimiento: yup
    .string()
    .nullable()
    .default(null),
});

type FormData = yup.InferType<typeof validationSchema>;

interface PersonFormProps {
  person?: Person;
  onSubmit: (data: PersonFormType) => Promise<void>;
  onCancel: () => void;
  isEditing?: boolean;
  loading?: boolean;
}

const PersonForm: React.FC<PersonFormProps> = ({
  person,
  onSubmit,
  onCancel,
  isEditing = false,
  loading = false,
}) => {
  const [rutValidation, setRutValidation] = useState<RutValidation>({
    rut: '',
    isValid: false,
    formatted: '',
  });
  const [submitError, setSubmitError] = useState<string | null>(null);

  const {
    control,
    handleSubmit,
    formState: { errors, isValid, isDirty },
    watch,
    setValue,
    reset,
  } = useForm<FormData>({
    resolver: yupResolver(validationSchema),
    defaultValues: {
      rut: person?.rut || '',
      nombre: person?.nombre || '',
      apellido: person?.apellido || '',
      religion: '',
      email: person?.email || null,
      telefono: person?.telefono || null,
      direccion: person?.direccion || null,
      fecha_nacimiento: person?.fecha_nacimiento || null,
    },
    mode: 'onChange',
  });

  const watchedRut = watch('rut');

  // Validar RUT en tiempo real
  useEffect(() => {
    if (watchedRut) {
      const isValid = validateRut(watchedRut);
      const formatted = formatRut(watchedRut);
      setRutValidation({
        rut: watchedRut,
        isValid,
        formatted,
        message: isValid ? 'RUT válido' : 'RUT inválido',
      });
    }
  }, [watchedRut]);

  const handleFormSubmit = async (data: FormData) => {
    try {
      setSubmitError(null);
      
      // Procesar datos antes de enviar
      const processedData = {
        ...data,
        rut: rutValidation.formatted, // Usar RUT formateado
        religion: data.religion, // Enviar religión como texto plano
        email: data.email || null,
        telefono: data.telefono || null,
        direccion: data.direccion || null,
        fecha_nacimiento: data.fecha_nacimiento || null,
      };
      
      await onSubmit(processedData as PersonFormType);
    } catch (error: any) {
      setSubmitError(error.message || 'Error al guardar la persona');
    }
  };

  const handleRutChange = (value: string) => {
    const cleanValue = value.replace(/[^0-9kK]/g, '');
    setValue('rut', cleanValue, { shouldValidate: true });
  };

  return (
    <Card
      component={motion.div}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      sx={{ maxWidth: 800, mx: 'auto', mt: 2 }}
    >
      <CardContent>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <PersonIcon />
          {isEditing ? 'Editar Persona' : 'Registrar Nueva Persona'}
        </Typography>
        
        <Divider sx={{ mb: 3 }} />

        <AnimatePresence>
          {submitError && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
            >
              <Alert severity="error" sx={{ mb: 2 }}>
                {submitError}
              </Alert>
            </motion.div>
          )}
        </AnimatePresence>

        <Box component="form" onSubmit={handleSubmit(handleFormSubmit)} noValidate>
          <Stack spacing={3}>
            {/* Fila 1: RUT y Nombre */}
            <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', md: 'row' } }}>
              <Box sx={{ flex: 1 }}>
                <Controller
                  name="rut"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="RUT"
                      fullWidth
                      error={!!errors.rut}
                      helperText={errors.rut?.message}
                      onChange={(e) => handleRutChange(e.target.value)}
                      value={rutValidation.formatted}
                      InputProps={{
                        startAdornment: (
                          <InputAdornment position="start">
                            <PersonIcon />
                          </InputAdornment>
                        ),
                        endAdornment: (
                          <InputAdornment position="end">
                            {rutValidation.isValid ? (
                              <CheckCircleIcon color="success" />
                            ) : watchedRut ? (
                              <ErrorIcon color="error" />
                            ) : null}
                          </InputAdornment>
                        ),
                      }}
                    />
                  )}
                />
              </Box>

              <Box sx={{ flex: 1 }}>
                <Controller
                  name="nombre"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Nombre"
                      fullWidth
                      error={!!errors.nombre}
                      helperText={errors.nombre?.message}
                    />
                  )}
                />
              </Box>
            </Box>

            {/* Fila 2: Apellido y Religión */}
            <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', md: 'row' } }}>
              <Box sx={{ flex: 1 }}>
                <Controller
                  name="apellido"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Apellido"
                      fullWidth
                      error={!!errors.apellido}
                      helperText={errors.apellido?.message}
                    />
                  )}
                />
              </Box>

              <Box sx={{ flex: 1 }}>
                <Controller
                  name="religion"
                  control={control}
                  render={({ field }) => (
                    <FormControl fullWidth error={!!errors.religion}>
                      <InputLabel>Religión</InputLabel>
                      <Select
                        {...field}
                        label="Religión"
                      >
                        {RELIGION_OPTIONS.map((option) => (
                          <MenuItem key={option.value} value={option.value}>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Typography>{option.label}</Typography>
                              <Chip
                                label={option.category}
                                size="small"
                                color="primary"
                                variant="outlined"
                              />
                            </Box>
                          </MenuItem>
                        ))}
                      </Select>
                      {errors.religion && (
                        <Typography variant="caption" color="error" sx={{ mt: 1 }}>
                          {errors.religion.message}
                        </Typography>
                      )}
                    </FormControl>
                  )}
                />
              </Box>
            </Box>

            {/* Fila 3: Email y Teléfono */}
            <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', md: 'row' } }}>
              <Box sx={{ flex: 1 }}>
                <Controller
                  name="email"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Email"
                      type="email"
                      fullWidth
                      error={!!errors.email}
                      helperText={errors.email?.message}
                      InputProps={{
                        startAdornment: (
                          <InputAdornment position="start">
                            <EmailIcon />
                          </InputAdornment>
                        ),
                      }}
                    />
                  )}
                />
              </Box>

              <Box sx={{ flex: 1 }}>
                <Controller
                  name="telefono"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Teléfono"
                      fullWidth
                      error={!!errors.telefono}
                      helperText={errors.telefono?.message}
                      InputProps={{
                        startAdornment: (
                          <InputAdornment position="start">
                            <PhoneIcon />
                          </InputAdornment>
                        ),
                      }}
                    />
                  )}
                />
              </Box>
            </Box>

            {/* Fila 4: Dirección */}
            <Box>
              <Controller
                name="direccion"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Dirección"
                    fullWidth
                    multiline
                    rows={2}
                    error={!!errors.direccion}
                    helperText={errors.direccion?.message}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <LocationOnIcon />
                        </InputAdornment>
                      ),
                    }}
                  />
                )}
              />
            </Box>

            {/* Fila 5: Fecha de Nacimiento */}
            <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', md: 'row' } }}>
              <Box sx={{ flex: 1 }}>
                <Controller
                  name="fecha_nacimiento"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Fecha de Nacimiento"
                      type="date"
                      fullWidth
                      error={!!errors.fecha_nacimiento}
                      helperText={errors.fecha_nacimiento?.message}
                      InputLabelProps={{
                        shrink: true,
                      }}
                      InputProps={{
                        startAdornment: (
                          <InputAdornment position="start">
                            <CalendarTodayIcon />
                          </InputAdornment>
                        ),
                      }}
                    />
                  )}
                />
              </Box>
              <Box sx={{ flex: 1 }}></Box>
            </Box>
          </Stack>

          {/* Lista de religiones disponibles */}
          <Box sx={{ mt: 3, p: 2, bgcolor: 'background.paper', borderRadius: 1, border: 1, borderColor: 'divider' }}>
            <Typography variant="h6" gutterBottom>
              Religiones Disponibles
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {RELIGION_OPTIONS.map((option) => (
                <Chip
                  key={option.value}
                  label={option.label}
                  variant="outlined"
                  size="small"
                  onClick={() => setValue('religion', option.value)}
                  sx={{ cursor: 'pointer' }}
                />
              ))}
            </Box>
          </Box>
        </Box>
      </CardContent>

      <CardActions sx={{ justifyContent: 'flex-end', p: 2 }}>
        <Button
          onClick={onCancel}
          variant="outlined"
          disabled={loading}
        >
          Cancelar
        </Button>
        <Button
          onClick={handleSubmit(handleFormSubmit)}
          variant="contained"
          disabled={!isValid || !isDirty || loading}
          startIcon={loading && <CircularProgress size={20} />}
        >
          {loading ? 'Guardando...' : isEditing ? 'Actualizar' : 'Registrar'}
        </Button>
      </CardActions>
    </Card>
  );
};

export default PersonForm;
