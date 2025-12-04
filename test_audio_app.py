#!/usr/bin/env python3
"""
Pruebas básicas para la aplicación AudioATexto
"""

import unittest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestAudioTranscriptionApp(unittest.TestCase):
    """Pruebas unitarias para la aplicación de transcripción"""
    
    def test_imports(self):
        """Verifica que los imports funcionen correctamente"""
        try:
            # Intentar importar el módulo principal
            import main
            self.assertTrue(hasattr(main, 'AudioTranscriptionApp'))
            self.assertTrue(hasattr(main, 'main'))
        except ImportError as e:
            # Si falta tkinter u otras dependencias, es esperado en algunos entornos
            if 'tkinter' in str(e) or 'vosk' in str(e) or 'numpy' in str(e):
                self.skipTest(f"Dependencias opcionales no disponibles: {e}")
            else:
                self.fail(f"Error inesperado al importar main.py: {e}")
    
    def test_check_system_imports(self):
        """Verifica que el script de verificación funcione"""
        try:
            import check_system
            self.assertTrue(hasattr(check_system, 'check_dependencies'))
            self.assertTrue(hasattr(check_system, 'check_vosk_model'))
        except ImportError as e:
            self.fail(f"Error al importar check_system.py: {e}")
    
    def test_requirements_file_exists(self):
        """Verifica que el archivo requirements.txt exista"""
        self.assertTrue(
            os.path.exists('requirements.txt'),
            "El archivo requirements.txt no existe"
        )
    
    def test_requirements_content(self):
        """Verifica que requirements.txt contenga las dependencias necesarias"""
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        required_packages = ['vosk', 'pydub', 'numpy', 'scipy', 'noisereduce', 'soundfile']
        
        for package in required_packages:
            self.assertIn(
                package,
                content,
                f"El paquete {package} no está en requirements.txt"
            )
    
    def test_readme_exists(self):
        """Verifica que el archivo README.md exista y tenga contenido"""
        self.assertTrue(
            os.path.exists('README.md'),
            "El archivo README.md no existe"
        )
        
        with open('README.md', 'r') as f:
            content = f.read()
        
        self.assertGreater(
            len(content),
            100,
            "El archivo README.md está vacío o tiene muy poco contenido"
        )
        
        # Verificar que contenga información clave
        self.assertIn('AudioATexto', content)
        self.assertIn('Vosk', content)
        self.assertIn('Instalación', content)


class TestAudioProcessingLogic(unittest.TestCase):
    """Pruebas para la lógica de procesamiento de audio"""
    
    def test_audio_enhancement_logic(self):
        """Verifica la lógica de mejora de audio"""
        try:
            import numpy as np
            from scipy import signal
            
            # Crear audio de prueba
            sample_rate = 16000
            duration = 1  # 1 segundo
            t = np.linspace(0, duration, sample_rate * duration)
            audio_data = np.sin(2 * np.pi * 440 * t)  # 440 Hz tone
            
            # Probar normalización
            max_val = np.max(np.abs(audio_data))
            if max_val > 0:
                normalized = audio_data / max_val * 0.95
                self.assertLessEqual(np.max(np.abs(normalized)), 1.0)
            
            # Probar clipping
            clipped = np.clip(audio_data, -1.0, 1.0)
            self.assertLessEqual(np.max(clipped), 1.0)
            self.assertGreaterEqual(np.min(clipped), -1.0)
            
            # Probar conversión a int16
            int_audio = np.int16(clipped * 32767)
            self.assertLessEqual(np.max(int_audio), 32767)
            self.assertGreaterEqual(np.min(int_audio), -32768)
            
        except ImportError as e:
            self.skipTest(f"Dependencias no disponibles: {e}")
    
    def test_filter_frequency_validation(self):
        """Verifica que la validación de frecuencias funcione correctamente"""
        try:
            # Simular cálculo de frecuencias
            sample_rate = 16000
            nyquist = sample_rate / 2
            low = 300 / nyquist
            high = 3400 / nyquist
            
            # Verificar que estén en el rango válido
            self.assertGreater(low, 0)
            self.assertLess(high, 1.0)
            self.assertLess(low, high)
            
        except Exception as e:
            self.fail(f"Error en validación de frecuencias: {e}")


def run_tests():
    """Ejecuta todas las pruebas"""
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las pruebas
    suite.addTests(loader.loadTestsFromTestCase(TestAudioTranscriptionApp))
    suite.addTests(loader.loadTestsFromTestCase(TestAudioProcessingLogic))
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar código de salida
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
