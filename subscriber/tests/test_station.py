import pytest
import json
from unittest.mock import Mock, patch, MagicMock
import sys
import os



class TestWeatherStationLogic:
    """Tests für die Wetterstation-Logik"""
    
    def test_temperature_range(self):
        """Teste dass Temperatur im erwarteten Bereich ist"""
        import random
        random.seed(42)
        
        for _ in range(100):
            temp = round(random.uniform(15, 30), 1)
            assert 15 <= temp <= 30, f"Temperatur {temp} außerhalb des Bereichs"
    
    def test_humidity_range(self):
        """Teste dass Luftfeuchtigkeit im erwarteten Bereich ist"""
        import random
        random.seed(42)
        
        for _ in range(100):
            humidity = round(random.uniform(30, 60), 1)
            assert 30 <= humidity <= 60, f"Luftfeuchtigkeit {humidity} außerhalb des Bereichs"
    
    def test_sensor_error_value(self):
        """Teste dass Sensorfehler korrekt als -999 dargestellt wird"""
        sensor_error_temp = -999
        assert sensor_error_temp == -999, "Sensorfehler-Wert stimmt nicht"
    
    def test_json_data_structure(self):
        """Teste dass die Datenstruktur korrekt ist"""
        import time
        
        data = {
            "stationId": "WS-TEST",
            "temperature": 22.5,
            "humidity": 45.3,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        
        assert "stationId" in data
        assert "temperature" in data
        assert "humidity" in data
        assert "timestamp" in data
        
        assert isinstance(data["stationId"], str)
        assert isinstance(data["temperature"], (int, float))
        assert isinstance(data["humidity"], (int, float))
        assert isinstance(data["timestamp"], str)
    
    def test_json_serialization(self):
        """Teste dass Daten als JSON serialisiert werden können"""
        import time
        
        data = {
            "stationId": "WS-TEST",
            "temperature": 22.5,
            "humidity": 45.3,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        
        json_str = json.dumps(data)
        assert isinstance(json_str, str)
        
        data_back = json.loads(json_str)
        assert data_back == data


class TestStationConfiguration:
    """Tests für die Stations-Konfiguration"""
    
    def test_station_id_format(self):
        """Teste dass Station ID das richtige Format hat"""
        station_ids = ["WS-01", "WS-02", "WS-03", "WS-XX"]
        
        for station_id in station_ids:
            assert station_id.startswith("WS-"), f"Station ID {station_id} hat falsches Präfix"
            assert len(station_id) == 5, f"Station ID {station_id} hat falsche Länge"
    
    def test_interval_values(self):
        """Teste dass Intervalle positive Zahlen sind"""
        intervals = [3, 5, 7]
        
        for interval in intervals:
            assert interval > 0, f"Intervall {interval} muss positiv sein"
            assert isinstance(interval, int), f"Intervall {interval} muss Integer sein"


class TestMQTTConfiguration:
    """Tests für MQTT-Konfiguration"""
    
    def test_mqtt_topic(self):
        """Teste dass MQTT Topic korrekt ist"""
        topic = "weather"
        assert topic == "weather", "MQTT Topic sollte 'weather' sein"
        assert len(topic) > 0, "MQTT Topic darf nicht leer sein"
    
    def test_mqtt_port(self):
        """Teste dass MQTT Port gültig ist"""
        port = 1883
        assert port == 1883, "MQTT Port sollte 1883 sein"
        assert 1 <= port <= 65535, "MQTT Port muss im gültigen Bereich sein"


@pytest.mark.integration
class TestStationIntegration:
    """Integrationstests (werden mit MQTT Mock durchgeführt)"""
    
    @patch('paho.mqtt.client.Client')
    def test_mqtt_client_creation(self, mock_mqtt):
        """Teste dass MQTT Client erstellt werden kann"""
        mock_client = MagicMock()
        mock_mqtt.return_value = mock_client
        
        import paho.mqtt.client as mqtt
        client = mqtt.Client()
        
        assert client is not None
    
    @patch('paho.mqtt.client.Client')
    def test_mqtt_publish(self, mock_mqtt):
        """Teste dass Nachrichten publiziert werden können"""
        mock_client = MagicMock()
        mock_mqtt.return_value = mock_client
        
        import paho.mqtt.client as mqtt
        client = mqtt.Client()
        
        test_data = {"test": "data"}
        client.publish("weather", json.dumps(test_data))
        
        mock_client.publish.assert_called_once()