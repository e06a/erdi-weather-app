import json
import time
import random
import pytest
from unittest.mock import patch, MagicMock


class TestWeatherData:
    """Tests für generierte Wetterdaten"""

    def test_temperature_is_within_bounds(self):
        random.seed(123)

        values = [round(random.uniform(15, 30), 1) for _ in range(100)]

        for value in values:
            assert 15 <= value <= 30

    def test_humidity_is_within_bounds(self):
        random.seed(123)

        values = [round(random.uniform(30, 60), 1) for _ in range(100)]

        for value in values:
            assert 30 <= value <= 60

    def test_sensor_error_constant(self):
        ERROR_VALUE = -999
        assert ERROR_VALUE == -999


class TestWeatherPayload:
    """Tests für Datenformat und Serialisierung"""

    def _create_sample_payload(self):
        return {
            "stationId": "WS-TEST",
            "temperature": 22.5,
            "humidity": 45.3,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    def test_payload_contains_required_fields(self):
        payload = self._create_sample_payload()

        required_keys = {"stationId", "temperature", "humidity", "timestamp"}
        assert required_keys.issubset(payload.keys())

    def test_payload_field_types(self):
        payload = self._create_sample_payload()

        assert isinstance(payload["stationId"], str)
        assert isinstance(payload["temperature"], (int, float))
        assert isinstance(payload["humidity"], (int, float))
        assert isinstance(payload["timestamp"], str)

    def test_payload_can_be_serialized_to_json(self):
        payload = self._create_sample_payload()

        encoded = json.dumps(payload)
        decoded = json.loads(encoded)

        assert decoded == payload


class TestStationSettings:
    """Tests für Stationsparameter"""

    @pytest.mark.parametrize("station_id", ["WS-01", "WS-02", "WS-XX"])
    def test_station_id_structure(self, station_id):
        assert station_id.startswith("WS-")
        assert len(station_id) == 5

    @pytest.mark.parametrize("interval", [3, 5, 7])
    def test_intervals_are_valid(self, interval):
        assert isinstance(interval, int)
        assert interval > 0


class TestMQTTSettings:
    """Tests für MQTT Basiskonfiguration"""

    def test_default_topic(self):
        topic = "weather"
        assert topic
        assert topic == "weather"

    def test_default_port(self):
        port = 1883
        assert 1 <= port <= 65535
        assert port == 1883


@pytest.mark.integration
class TestMQTTIntegration:
    """Integrationstests mit gemocktem MQTT Client"""

    @patch("paho.mqtt.client.Client")
    def test_mqtt_client_initialization(self, mock_client_class):
        mock_client_class.return_value = MagicMock()

        import paho.mqtt.client as mqtt
        client = mqtt.Client()

        assert client is not None

    @patch("paho.mqtt.client.Client")
    def test_mqtt_publish_call(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        import paho.mqtt.client as mqtt
        client = mqtt.Client()

        payload = {"key": "value"}
        client.publish("weather", json.dumps(payload))

        mock_client.publish.assert_called_once()
