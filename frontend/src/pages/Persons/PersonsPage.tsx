import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  InputAdornment,
  Alert,
  CircularProgress,
  Stack,
  Tooltip,
  Tabs,
  Tab,
  Pagination,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
  Person as PersonIcon,
  Refresh as RefreshIcon,
  Visibility as VisibilityIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { Person, PersonForm } from '../../types/persons';
import { personService } from '../../services/api';
import PersonFormSimple from '../../components/Forms/PersonFormSimple';
import RutSearchForm from '../../components/Forms/RutSearchForm';
import PersonDetailCard from '../../components/UI/PersonDetailCard';

const PersonsPage: React.FC = () => {
  const [persons, setPersons] = useState<Person[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedPerson, setSelectedPerson] = useState<Person | null>(null);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [personToDelete, setPersonToDelete] = useState<Person | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [tabValue, setTabValue] = useState(0);
  const [foundPerson, setFoundPerson] = useState<Person | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [detailDialogOpen, setDetailDialogOpen] = useState(false);
  const [personDetail, setPersonDetail] = useState<Person | null>(null);

  // Cargar personas al montar el componente
  useEffect(() => {
    loadPersons();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const loadPersons = async (pageNum: number = 1) => {
    try {
      setLoading(true);
      setError(null);
      const response = await personService.getPersons({
        page: pageNum,
        per_page: 10,
        search: searchQuery || undefined,
      });
      
      // La respuesta ya está normalizada en el servicio
        
      setPersons(response.items || []);
      setTotalPages(response.pages || 1);
      setPage(pageNum);
    } catch (err: any) {
      setError(err.message || 'Error al cargar las personas');
    } finally {
      setLoading(false);
    }
  };

  const handlePersonFound = (person: Person) => {
    setFoundPerson(person);
    setError(null);
  };

  const handleRutSearchError = (error: string) => {
    setFoundPerson(null);
    setError(error);
  };

  const handleViewDetails = async (person: Person) => {
    try {
      const response = await personService.getPerson(person.id);
      // El servicio ya normaliza la respuesta
      setPersonDetail(response);
      setDetailDialogOpen(true);
    } catch (err: any) {
      setError(err.message || 'Error al cargar los detalles');
    }
  };

  const handlePageChange = (_: React.ChangeEvent<unknown>, value: number) => {
    loadPersons(value);
  };

  const handleTabChange = (_: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
    setError(null);
    setFoundPerson(null);
  };

  const handleAddPerson = () => {
    setSelectedPerson(null);
    setIsEditing(false);
    setIsFormOpen(true);
  };

  const handleEditPerson = (person: Person) => {
    setSelectedPerson(person);
    setIsEditing(true);
    setIsFormOpen(true);
  };

  const handleDeletePerson = (person: Person) => {
    setPersonToDelete(person);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = async () => {
    if (!personToDelete) return;

    try {
      setSubmitting(true);
      const response = await personService.deletePerson(personToDelete.id);
      if (response.success) {
        setPersons(persons.filter(p => p.id !== personToDelete.id));
        setDeleteDialogOpen(false);
        setPersonToDelete(null);
      } else {
        setError(response.message || 'Error al eliminar la persona');
      }
    } catch (err: any) {
      setError(err.message || 'Error al eliminar la persona');
    } finally {
      setSubmitting(false);
    }
  };

  const handleFormSubmit = async (data: PersonForm) => {
    try {
      setSubmitting(true);
      setError(null);

      if (isEditing && selectedPerson) {
        const response = await personService.updatePerson(selectedPerson.id, data);
        if (response.success) {
          setPersons(persons.map(p => p.id === selectedPerson.id ? response.data : p));
          setIsFormOpen(false);
          setSelectedPerson(null);
        } else {
          setError(response.message || 'Error al actualizar la persona');
        }
      } else {
        const response = await personService.createPerson(data);
        if (response.success) {
          setPersons([...persons, response.data]);
          setIsFormOpen(false);
        } else {
          setError(response.message || 'Error al crear la persona');
        }
      }
    } catch (err: any) {
      setError(err.message || 'Error al guardar la persona');
    } finally {
      setSubmitting(false);
    }
  };

  const handleFormCancel = () => {
    setIsFormOpen(false);
    setSelectedPerson(null);
    setIsEditing(false);
  };

  const handleSearch = async () => {
    loadPersons(1);
  };

  const formatRut = (rut: string): string => {
    // El RUT viene ofuscado del backend (rut)
    return rut;
  };

  if (loading && persons.length === 0) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ 
        mb: 4, 
        p: 3, 
        borderRadius: 3, 
        background: 'linear-gradient(135deg, #1e293b 0%, #334155 100%)',
        border: '1px solid #475569',
        position: 'relative',
        overflow: 'hidden',
      }}>
        <Box sx={{ position: 'relative', zIndex: 2 }}>
          <Stack direction="row" justifyContent="space-between" alignItems="center">
            <Box>
              <Typography variant="h4" component="h1" sx={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: 1,
                fontWeight: 700,
                color: '#f8fafc',
                mb: 1
              }}>
                <PersonIcon sx={{ color: '#3b82f6' }} />
                Gestión de Personas
              </Typography>
              <Typography variant="body1" sx={{ color: '#94a3b8' }}>
                Administración del sistema CRUD de personas con validación de RUT
              </Typography>
            </Box>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={handleAddPerson}
              sx={{ 
                minWidth: 150,
                background: `linear-gradient(135deg, #3b82f6, #8b5cf6)`,
                '&:hover': {
                  background: `linear-gradient(135deg, #2563eb, #7c3aed)`,
                  transform: 'translateY(-2px)',
                  boxShadow: '0 8px 20px rgba(59, 130, 246, 0.3)',
                },
                transition: 'all 0.3s ease',
              }}
            >
              Nueva Persona
            </Button>
          </Stack>
        </Box>
        <Box sx={{ 
          position: 'absolute', 
          top: 0, 
          right: 0, 
          width: '200px', 
          height: '200px', 
          background: 'rgba(59, 130, 246, 0.1)', 
          borderRadius: '50%',
          transform: 'translate(50%, -50%)',
        }} />
      </Box>

      <AnimatePresence>
        {error && tabValue === 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
          >
            <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
              {error}
            </Alert>
          </motion.div>
        )}
      </AnimatePresence>

      <Card sx={{ 
        mb: 3,
        background: 'linear-gradient(145deg, #1e293b 0%, #334155 100%)',
        border: '1px solid #475569',
        borderRadius: '12px',
        overflow: 'visible'
      }}>
        <CardContent sx={{ p: 3 }}>
          <Tabs 
            value={tabValue} 
            onChange={handleTabChange} 
            sx={{ 
              mb: 3,
              '& .MuiTabs-indicator': {
                backgroundColor: '#3b82f6',
              },
              '& .MuiTab-root': {
                color: '#94a3b8',
                fontWeight: 600,
                '&.Mui-selected': {
                  color: '#3b82f6',
                },
              },
            }}
          >
            <Tab label="Lista de Personas" />
            <Tab label="Búsqueda por RUT" />
          </Tabs>

          {tabValue === 0 && (
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" sx={{ color: '#f8fafc', mb: 2, fontWeight: 600 }}>
                Buscar Personas
              </Typography>
              <Stack direction="row" spacing={2} alignItems="center">
                <TextField
                  placeholder="Buscar por RUT, nombre, apellido o email..."
                  variant="outlined"
                  size="small"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  sx={{
                    flexGrow: 1,
                    '& .MuiOutlinedInput-root': {
                      backgroundColor: 'rgba(15, 23, 42, 0.8)',
                      borderRadius: '8px',
                      '& fieldset': {
                        borderColor: '#475569',
                      },
                      '&:hover fieldset': {
                        borderColor: '#3b82f6',
                      },
                      '&.Mui-focused fieldset': {
                        borderColor: '#3b82f6',
                      },
                    },
                    '& .MuiInputBase-input': {
                      color: '#f1f5f9',
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
                  variant="contained"
                  onClick={handleSearch}
                  disabled={loading}
                  startIcon={<SearchIcon />}
                  sx={{
                    background: '#3b82f6',
                    '&:hover': {
                      background: '#2563eb',
                    },
                    '&:disabled': {
                      background: '#475569',
                      color: '#94a3b8',
                    },
                  }}
                >
                  Buscar
                </Button>
                <Tooltip title="Actualizar lista">
                  <IconButton
                    onClick={() => loadPersons()} 
                    disabled={loading}
                    sx={{
                      color: '#94a3b8',
                      backgroundColor: '#1e293b',
                      border: '1px solid #475569',
                      borderRadius: '8px',
                      '&:hover': {
                        color: '#3b82f6',
                        backgroundColor: '#334155',
                        borderColor: '#3b82f6',
                      },
                      '&:disabled': {
                        color: '#64748b',
                        backgroundColor: '#0f172a',
                      },
                    }}
                  >
                    <RefreshIcon />
                  </IconButton>
                </Tooltip>
              </Stack>
            </Box>
          )}

          {tabValue === 1 && (
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" sx={{ color: '#f8fafc', mb: 3, fontWeight: 600 }}>
                Búsqueda por RUT
              </Typography>
              <Box sx={{ 
                backgroundColor: 'rgba(15, 23, 42, 0.8)', 
                borderRadius: '12px', 
                border: '1px solid #475569',
                p: 3,
                mb: 3
              }}>
                <RutSearchForm
                  onPersonFound={handlePersonFound}
                  onError={handleRutSearchError}
                />
              </Box>
              
              <AnimatePresence>
                {foundPerson && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, height: 0 }}
                    transition={{ duration: 0.4, type: 'spring', stiffness: 100 }}
                  >
                    <Typography variant="h6" sx={{ color: '#f8fafc', mb: 2, fontWeight: 600 }}>
                      Información de la Persona
                    </Typography>
                    <Box sx={{ 
                      backgroundColor: 'rgba(15, 23, 42, 0.8)', 
                      borderRadius: '12px', 
                      border: '1px solid #475569',
                      p: 3
                    }}>
                      <PersonDetailCard
                        person={foundPerson}
                        onEdit={handleEditPerson}
                        onDelete={handleDeletePerson}
                      />
                    </Box>
                  </motion.div>
                )}
              </AnimatePresence>
            </Box>
          )}
        </CardContent>
      </Card>

      {tabValue === 0 && (
        <>
          <TableContainer 
            component={Paper}
            sx={{
              background: 'linear-gradient(145deg, #1e293b 0%, #334155 100%)',
              border: '1px solid #475569',
              borderRadius: 3,
            }}
          >
            <Table>
              <TableHead sx={{ backgroundColor: '#334155' }}>
                <TableRow>
                  <TableCell sx={{ color: '#f8fafc', fontWeight: 600 }}>RUT</TableCell>
                  <TableCell sx={{ color: '#f8fafc', fontWeight: 600 }}>Nombre</TableCell>
                  <TableCell sx={{ color: '#f8fafc', fontWeight: 600 }}>Apellido</TableCell>
                  <TableCell sx={{ color: '#f8fafc', fontWeight: 600 }}>Email</TableCell>
                  <TableCell sx={{ color: '#f8fafc', fontWeight: 600 }}>Teléfono</TableCell>
                  <TableCell sx={{ color: '#f8fafc', fontWeight: 600 }}>Fecha Registro</TableCell>
                  <TableCell align="center" sx={{ color: '#f8fafc', fontWeight: 600 }}>Acciones</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loading ? (
                  <TableRow>
                    <TableCell colSpan={7} align="center" sx={{ color: '#94a3b8', py: 4 }}>
                      <CircularProgress size={24} />
                    </TableCell>
                  </TableRow>
                ) : persons.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={7} align="center" sx={{ color: '#94a3b8', py: 4 }}>
                      <Typography variant="body1">
                        No hay personas registradas
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  persons.map((person) => (
                    <TableRow
                      key={person.id}
                      component={motion.tr}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.3 }}
                      sx={{
                        '&:hover': {
                          backgroundColor: 'rgba(255,255,255,0.05)',
                        },
                      }}
                    >
                      <TableCell sx={{ color: '#f8fafc' }}>
                        <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                          {formatRut(person.rut_masked)}
                        </Typography>
                      </TableCell>
                      <TableCell sx={{ color: '#f8fafc' }}>{person.nombre}</TableCell>
                      <TableCell sx={{ color: '#f8fafc' }}>{person.apellido}</TableCell>
                      <TableCell sx={{ color: '#94a3b8' }}>{person.email || '-'}</TableCell>
                      <TableCell sx={{ color: '#94a3b8' }}>{person.telefono || '-'}</TableCell>
                      <TableCell sx={{ color: '#94a3b8' }}>
                        {person.created_at ? new Date(person.created_at).toLocaleDateString('es-ES') : '-'}
                      </TableCell>
                      <TableCell align="center">
                        <Stack direction="row" spacing={1} justifyContent="center">
                          <Tooltip title="Ver detalles">
                            <IconButton
                              size="small"
                              onClick={() => handleViewDetails(person)}
                              sx={{
                                color: '#06b6d4',
                                '&:hover': {
                                  backgroundColor: 'rgba(6, 182, 212, 0.1)',
                                },
                              }}
                            >
                              <VisibilityIcon />
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Editar">
                            <IconButton
                              size="small"
                              onClick={() => handleEditPerson(person)}
                              sx={{
                                color: '#3b82f6',
                                '&:hover': {
                                  backgroundColor: 'rgba(59, 130, 246, 0.1)',
                                },
                              }}
                            >
                              <EditIcon />
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Eliminar">
                            <IconButton
                              size="small"
                              onClick={() => handleDeletePerson(person)}
                              sx={{
                                color: '#ef4444',
                                '&:hover': {
                                  backgroundColor: 'rgba(239, 68, 68, 0.1)',
                                },
                              }}
                            >
                              <DeleteIcon />
                            </IconButton>
                          </Tooltip>
                        </Stack>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>

          {totalPages > 1 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
              <Pagination
                count={totalPages}
                page={page}
                onChange={handlePageChange}
                color="primary"
                showFirstButton
                showLastButton
              />
            </Box>
          )}
        </>
      )}

      {/* Diálogo de formulario */}
      <Dialog
        open={isFormOpen}
        onClose={handleFormCancel}
        maxWidth="md"
        fullWidth
        PaperProps={{
          component: motion.div,
          initial: { opacity: 0, scale: 0.9 },
          animate: { opacity: 1, scale: 1 },
          exit: { opacity: 0, scale: 0.9 },
        }}
      >
        <DialogContent sx={{ p: 0 }}>
          <PersonFormSimple
            person={selectedPerson || undefined}
            onSubmit={handleFormSubmit}
            onCancel={handleFormCancel}
            isEditing={isEditing}
            loading={submitting}
          />
        </DialogContent>
      </Dialog>

      {/* Diálogo de confirmación de eliminación */}
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          Confirmar Eliminación
        </DialogTitle>
        <DialogContent>
          <Typography>
            ¿Está seguro que desea eliminar a {personToDelete?.nombre} {personToDelete?.apellido}?
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Esta acción no se puede deshacer.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)} disabled={submitting}>
            Cancelar
          </Button>
          <Button
            onClick={confirmDelete}
            color="error"
            variant="contained"
            disabled={submitting}
            startIcon={submitting && <CircularProgress size={20} />}
          >
            {submitting ? 'Eliminando...' : 'Eliminar'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Diálogo de detalles de persona */}
      <Dialog
        open={detailDialogOpen}
        onClose={() => setDetailDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogContent sx={{ p: 2 }}>
          {personDetail && (
            <Box sx={{ p: 1 }}>
              {tabValue === 1 ? (
                <PersonDetailCard
                  person={personDetail}
                  onEdit={handleEditPerson}
                  onDelete={handleDeletePerson}
                />
              ) : (
                <PersonDetailCard
                  person={personDetail}
                  onEdit={handleEditPerson}
                  onDelete={handleDeletePerson}
                />
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDetailDialogOpen(false)}>
            Cerrar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PersonsPage;
