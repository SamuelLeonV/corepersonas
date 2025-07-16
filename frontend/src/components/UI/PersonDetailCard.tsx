import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Stack,
  Divider,
  Avatar,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Person as PersonIcon,
  Email as EmailIcon,
  Phone as PhoneIcon,
  LocationOn as LocationIcon,
  CalendarToday as CalendarIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Security as SecurityIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { Person } from '../../types/persons';

interface PersonDetailCardProps {
  person: Person;
  onEdit?: (person: Person) => void;
  onDelete?: (person: Person) => void;
  showActions?: boolean;
}

const PersonDetailCard: React.FC<PersonDetailCardProps> = ({
  person,
  onEdit,
  onDelete,
  showActions = true,
}) => {
  const formatDate = (dateString: string | null) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const formatDateTime = (dateString: string) => {
    return new Date(dateString).toLocaleString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getInitials = (nombre: string, apellido: string) => {
    return `${nombre.charAt(0)}${apellido.charAt(0)}`.toUpperCase();
  };

  return (
    <Card
      component={motion.div}
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      sx={{ mb: 2 }}
    >
      <CardContent>
        <Stack direction="row" justifyContent="space-between" alignItems="flex-start" mb={2}>
          <Stack direction="row" spacing={2} alignItems="center">
            <Avatar sx={{ width: 56, height: 56, bgcolor: 'primary.main' }}>
              {getInitials(person.nombre, person.apellido)}
            </Avatar>
            <Box>
              <Typography variant="h5" component="h2">
                {person.nombre} {person.apellido}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ fontFamily: 'monospace' }}>
                RUT: {person.rut_masked}
              </Typography>
            </Box>
          </Stack>
          
          {showActions && (
            <Stack direction="row" spacing={1}>
              {onEdit && (
                <Tooltip title="Editar">
                  <IconButton onClick={() => onEdit(person)} color="primary">
                    <EditIcon />
                  </IconButton>
                </Tooltip>
              )}
              {onDelete && (
                <Tooltip title="Eliminar">
                  <IconButton onClick={() => onDelete(person)} color="error">
                    <DeleteIcon />
                  </IconButton>
                </Tooltip>
              )}
            </Stack>
          )}
        </Stack>

        <Divider sx={{ my: 2 }} />

        <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 2 }}>
          {/* Información de contacto */}
          <Box>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <PersonIcon />
              Información Personal
            </Typography>
            <Stack spacing={1}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <EmailIcon fontSize="small" color="action" />
                <Typography variant="body2">
                  {person.email || 'No especificado'}
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <PhoneIcon fontSize="small" color="action" />
                <Typography variant="body2">
                  {person.telefono || 'No especificado'}
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <LocationIcon fontSize="small" color="action" />
                <Typography variant="body2">
                  {person.direccion || 'No especificado'}
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <CalendarIcon fontSize="small" color="action" />
                <Typography variant="body2">
                  Nacimiento: {formatDate(person.fecha_nacimiento || null)}
                </Typography>
              </Box>
            </Stack>
          </Box>

          {/* Información sensible */}
          <Box>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <SecurityIcon />
              Información Protegida
            </Typography>
            <Stack spacing={1}>
              <Box>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Indicador de Religión (Hash):
                </Typography>
                <Chip
                  label={person.religion_indicator}
                  size="small"
                  sx={{ 
                    fontFamily: 'monospace',
                    backgroundColor: 'grey.100',
                    color: 'grey.700',
                    maxWidth: '100%',
                  }}
                />
              </Box>
            </Stack>
          </Box>

          {/* Información del sistema */}
          <Box>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <CalendarIcon />
              Información del Sistema
            </Typography>
            <Stack spacing={1}>
              <Typography variant="body2">
                <strong>Creado:</strong> {formatDateTime(person.created_at)}
              </Typography>
              {person.updated_at && (
                <Typography variant="body2">
                  <strong>Actualizado:</strong> {formatDateTime(person.updated_at)}
                </Typography>
              )}
              <Typography variant="body2">
                <strong>ID:</strong> {person.id}
              </Typography>
            </Stack>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default PersonDetailCard;
