import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { API_CONFIG, APP_CONFIG } from '../../config/env';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  FormControlLabel,
  Checkbox,
  Link,
  Alert,
  InputAdornment,
  IconButton,
  useTheme,
  Container,
  Avatar,
} from '@mui/material';
import {
  Visibility,
  VisibilityOff,
  Security,
  AccountCircle,
  Lock,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { authService } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';

const schema = yup.object().shape({
  email: yup.string().email('Email inválido').required('El email es requerido'),
  password: yup.string().min(6, 'La contraseña debe tener al menos 6 caracteres').required('La contraseña es requerida'),
});

const API_BASE_URL = API_CONFIG.BASE_URL;

const Login: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isAuthenticated } = useAuth();
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [loginError, setLoginError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Redirigir si ya está autenticado
  useEffect(() => {
    if (isAuthenticated) {
      const from = location.state?.from?.pathname || '/dashboard';
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, location]);

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  const handleLogin = async (data: any) => {
    setIsLoading(true);
    setLoginError('');

    try {
      const response = await authService.login(data.email, data.password);
      
      if (response.success) {
        localStorage.setItem('authToken', response.data.access_token);
        login(response.data.access_token, { email: data.email });
        const from = location.state?.from?.pathname || '/dashboard';
        navigate(from, { replace: true });
      } else {
        setLoginError(response.message || 'Error de autenticación');
      }
    } catch (error: any) {
      console.error('Error en login:', error);
      setLoginError(
        error.response?.data?.detail || 
        error.message || 
        'Error de conexión con el servidor'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%)',
        p: 2,
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Background decorative elements */}
      <Box sx={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: `
          radial-gradient(circle at 20% 80%, ${theme.palette.primary.main}15 0%, transparent 50%),
          radial-gradient(circle at 80% 20%, ${theme.palette.secondary.main}15 0%, transparent 50%),
          radial-gradient(circle at 40% 40%, ${theme.palette.info.main}10 0%, transparent 50%)
        `,
      }} />

      <Container maxWidth="sm" sx={{ position: 'relative', zIndex: 1 }}>
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <Card sx={{ 
            borderRadius: 4, 
            boxShadow: '0 25px 50px rgba(0,0,0,0.25)',
            overflow: 'hidden',
            background: 'linear-gradient(145deg, #1e293b 0%, #334155 100%)',
            border: '1px solid #475569',
          }}>
            {/* Header */}
            <Box sx={{ 
              background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
              color: 'white',
              p: 4,
              textAlign: 'center',
              position: 'relative',
              overflow: 'hidden',
            }}>
              <Box sx={{
                position: 'absolute',
                top: 0,
                right: 0,
                width: '150px',
                height: '150px',
                background: 'rgba(255,255,255,0.1)',
                borderRadius: '50%',
                transform: 'translate(30%, -30%)',
              }} />
              <Avatar sx={{ 
                bgcolor: 'rgba(255,255,255,0.2)', 
                width: 80, 
                height: 80, 
                margin: '0 auto 16px',
                position: 'relative',
                zIndex: 1,
                backdropFilter: 'blur(10px)',
              }}>
                <Security sx={{ fontSize: 40 }} />
              </Avatar>
              <Typography variant="h4" component="h1" gutterBottom sx={{ 
                fontWeight: 700,
                position: 'relative',
                zIndex: 1,
              }}>
                Sistema de Auditoría
              </Typography>
              <Typography variant="body1" sx={{ 
                opacity: 0.9,
                position: 'relative',
                zIndex: 1,
              }}>
                {APP_CONFIG.TITLE}
              </Typography>
              <Typography variant="caption" sx={{ 
                opacity: 0.6,
                position: 'relative',
                zIndex: 1,
              }}>
                v{APP_CONFIG.VERSION}
              </Typography>
            </Box>

            <CardContent sx={{ p: 4, backgroundColor: '#1e293b' }}>
              <form onSubmit={handleSubmit(handleLogin)}>
                <Typography variant="h5" component="h2" gutterBottom sx={{ 
                  fontWeight: 600,
                  color: '#f8fafc',
                  mb: 3,
                }}>
                  Iniciar Sesión
                </Typography>

                {loginError && (
                  <Alert 
                    severity="error" 
                    sx={{ 
                      mb: 2,
                      backgroundColor: '#fecaca',
                      color: '#991b1b',
                      border: '1px solid #f87171',
                      '& .MuiAlert-icon': {
                        color: '#dc2626'
                      }
                    }}
                  >
                    {loginError}
                  </Alert>
                )}

                <Controller
                  name="email"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Email"
                      type="email"
                      fullWidth
                      margin="normal"
                      error={!!errors.email}
                      helperText={errors.email?.message}
                      sx={{
                        mb: 2,
                        '& .MuiOutlinedInput-root': {
                          backgroundColor: 'rgba(255,255,255,0.05)',
                          '& fieldset': {
                            borderColor: '#475569',
                          },
                          '&:hover fieldset': {
                            borderColor: '#64748b',
                          },
                          '&.Mui-focused fieldset': {
                            borderColor: theme.palette.primary.main,
                          },
                        },
                        '& .MuiInputLabel-root': {
                          color: '#94a3b8',
                        },
                        '& .MuiInputBase-input': {
                          color: '#f8fafc',
                        },
                        '& .MuiFormHelperText-root': {
                          color: '#ef4444',
                        },
                      }}
                      InputProps={{
                        startAdornment: (
                          <InputAdornment position="start">
                            <AccountCircle sx={{ color: '#64748b' }} />
                          </InputAdornment>
                        ),
                      }}
                    />
                  )}
                />

                <Controller
                  name="password"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Contraseña"
                      type={showPassword ? 'text' : 'password'}
                      fullWidth
                      margin="normal"
                      error={!!errors.password}
                      helperText={errors.password?.message}
                      sx={{
                        mb: 2,
                        '& .MuiOutlinedInput-root': {
                          backgroundColor: 'rgba(255,255,255,0.05)',
                          '& fieldset': {
                            borderColor: '#475569',
                          },
                          '&:hover fieldset': {
                            borderColor: '#64748b',
                          },
                          '&.Mui-focused fieldset': {
                            borderColor: theme.palette.primary.main,
                          },
                        },
                        '& .MuiInputLabel-root': {
                          color: '#94a3b8',
                        },
                        '& .MuiInputBase-input': {
                          color: '#f8fafc',
                        },
                        '& .MuiFormHelperText-root': {
                          color: '#ef4444',
                        },
                      }}
                      InputProps={{
                        startAdornment: (
                          <InputAdornment position="start">
                            <Lock sx={{ color: '#64748b' }} />
                          </InputAdornment>
                        ),
                        endAdornment: (
                          <InputAdornment position="end">
                            <IconButton
                              onClick={handleClickShowPassword}
                              edge="end"
                              sx={{ color: '#64748b' }}
                            >
                              {showPassword ? <VisibilityOff /> : <Visibility />}
                            </IconButton>
                          </InputAdornment>
                        ),
                      }}
                    />
                  )}
                />

                <FormControlLabel
                  control={
                    <Checkbox
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                      sx={{
                        color: '#64748b',
                        '&.Mui-checked': {
                          color: theme.palette.primary.main,
                        },
                      }}
                    />
                  }
                  label={
                    <Typography sx={{ color: '#94a3b8' }}>
                      Recordarme
                    </Typography>
                  }
                  sx={{ mb: 3 }}
                />

                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  disabled={isLoading}
                  sx={{
                    mt: 2,
                    mb: 2,
                    py: 1.5,
                    fontWeight: 600,
                    fontSize: '1rem',
                    background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.light} 100%)`,
                    '&:hover': {
                      background: `linear-gradient(135deg, ${theme.palette.primary.dark} 0%, ${theme.palette.primary.main} 100%)`,
                      transform: 'translateY(-2px)',
                      boxShadow: '0 10px 20px rgba(0,0,0,0.2)',
                    },
                    '&:disabled': {
                      background: '#475569',
                      color: '#94a3b8',
                    },
                    transition: 'all 0.3s ease',
                  }}
                >
                  {isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
                </Button>

                <Box sx={{ textAlign: 'center', mt: 2 }}>
                  <Link
                    href="#"
                    variant="body2"
                    sx={{
                      color: theme.palette.primary.light,
                      textDecoration: 'none',
                      '&:hover': {
                        textDecoration: 'underline',
                      },
                    }}
                  >
                    ¿Olvidaste tu contraseña?
                  </Link>
                </Box>

                <Box sx={{ 
                  mt: 3, 
                  p: 2, 
                  backgroundColor: 'rgba(255,255,255,0.05)', 
                  borderRadius: 2,
                  border: '1px solid #334155',
                }}>
                  <Typography variant="body2" sx={{ color: '#94a3b8', mb: 1 }}>
                    <strong>Datos de prueba:</strong>
                  </Typography>
                  <Typography variant="body2" sx={{ color: '#94a3b8' }}>
                    Email: admin@auditoria.com
                  </Typography>
                  <Typography variant="body2" sx={{ color: '#94a3b8' }}>
                    Contraseña: admin123
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#64748b', mt: 1, display: 'block' }}>
                    API: {API_BASE_URL}
                  </Typography>
                </Box>
              </form>
            </CardContent>
          </Card>
        </motion.div>
      </Container>
    </Box>
  );
};

export default Login;
