import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { TemplateState, CreateTemplateData, Template } from '../types';
import { templateAPI } from '../services/api';

const initialState: TemplateState = {
  templates: [],
  selectedTemplate: null,
  loading: false,
  error: null,
};

// Async thunks
export const fetchTemplates = createAsyncThunk(
  'templates/fetchAll',
  async (_, { rejectWithValue }) => {
    try {
      const templates = await templateAPI.getAll();
      return templates;
    } catch (error: any) {
      return rejectWithValue(
        error.response?.data?.detail || 'Failed to fetch templates'
      );
    }
  }
);

export const fetchTemplateById = createAsyncThunk(
  'templates/fetchById',
  async (id: string, { rejectWithValue }) => {
    try {
      const template = await templateAPI.getById(id);
      return template;
    } catch (error: any) {
      return rejectWithValue(
        error.response?.data?.detail || 'Failed to fetch template'
      );
    }
  }
);

export const createTemplate = createAsyncThunk(
  'templates/create',
  async (templateData: CreateTemplateData, { rejectWithValue }) => {
    try {
      await templateAPI.create(templateData);
      return templateData;
    } catch (error: any) {
      return rejectWithValue(
        error.response?.data?.detail || 'Failed to create template'
      );
    }
  }
);

export const updateTemplate = createAsyncThunk(
  'templates/update',
  async (
    { id, templateData }: { id: string; templateData: Partial<CreateTemplateData> },
    { rejectWithValue }
  ) => {
    try {
      await templateAPI.update(id, templateData);
      return { id, templateData };
    } catch (error: any) {
      return rejectWithValue(
        error.response?.data?.detail || 'Failed to update template'
      );
    }
  }
);

export const deleteTemplate = createAsyncThunk(
  'templates/delete',
  async (id: string, { rejectWithValue }) => {
    try {
      await templateAPI.delete(id);
      return id;
    } catch (error: any) {
      return rejectWithValue(
        error.response?.data?.detail || 'Failed to delete template'
      );
    }
  }
);

const templateSlice = createSlice({
  name: 'templates',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setSelectedTemplate: (state, action: PayloadAction<Template | null>) => {
      state.selectedTemplate = action.payload;
    },
    clearSelectedTemplate: (state) => {
      state.selectedTemplate = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch all templates
      .addCase(fetchTemplates.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTemplates.fulfilled, (state, action) => {
        state.loading = false;
        state.templates = action.payload;
        state.error = null;
      })
      .addCase(fetchTemplates.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch template by ID
      .addCase(fetchTemplateById.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTemplateById.fulfilled, (state, action) => {
        state.loading = false;
        state.selectedTemplate = action.payload;
        state.error = null;
      })
      .addCase(fetchTemplateById.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Create template
      .addCase(createTemplate.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createTemplate.fulfilled, (state) => {
        state.loading = false;
        state.error = null;
      })
      .addCase(createTemplate.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Update template
      .addCase(updateTemplate.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateTemplate.fulfilled, (state) => {
        state.loading = false;
        state.error = null;
      })
      .addCase(updateTemplate.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Delete template
      .addCase(deleteTemplate.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteTemplate.fulfilled, (state, action) => {
        state.loading = false;
        state.templates = state.templates.filter(
          (template) => template._id !== action.payload
        );
        if (state.selectedTemplate?._id === action.payload) {
          state.selectedTemplate = null;
        }
        state.error = null;
      })
      .addCase(deleteTemplate.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError, setSelectedTemplate, clearSelectedTemplate } = templateSlice.actions;
export default templateSlice.reducer;
