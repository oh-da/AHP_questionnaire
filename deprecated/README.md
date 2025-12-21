# Deprecated Files

These files are from the old implementation and are no longer maintained.

## Deprecated Files

- **app.py**: Old Streamlit application
  - Replaced by: React frontend (`frontend/`)
  - Reason: Better UX, modern design, separation of concerns

- **api_server.py**: Old monolithic Flask API
  - Replaced by: SOLID-based backend (`backend/`)
  - Reason: Better architecture, maintainability, testability

- **requirements-streamlit.txt**: Streamlit dependencies
  - Replaced by: `requirements-backend.txt`

- **requirements-api.txt**: Old API dependencies
  - Replaced by: `requirements-backend.txt`

## Migration Guide

### If you were using the Streamlit app:
```bash
# Old way
streamlit run app.py

# New way
cd frontend && npm install && npm run dev
# Backend: python -m backend.main
```

### If you were using the old API:
```bash
# Old way
python api_server.py

# New way
python -m backend.main
```

## Why the change?

The new architecture follows **SOLID principles**:

1. ✅ **Single Responsibility**: Each class/module has one job
2. ✅ **Open/Closed**: Easy to extend without modifying existing code
3. ✅ **Liskov Substitution**: Implementations can be swapped
4. ✅ **Interface Segregation**: Small, focused interfaces
5. ✅ **Dependency Inversion**: Depend on abstractions, not implementations

This makes the code:
- More maintainable
- Easier to test
- Easier to extend
- More modular
- Better organized

---

Last updated: 2025-12-21
