import pytest
from worker.src.debtsimplifier import process_message, save_results_to_s3


def test_process_message_success(mocker):
    # Mocking the S3 client
    mock_s3 = mocker.MagicMock()
    mock_s3.get_object.return_value = {
        "Body": mocker.MagicMock(
            return_value=BytesIO(b"Kathy,Patrick,3359.0\nKathy,Ricky,2746.0\n")
        )
    }

    # Mocking the logger
    mock_logger = mocker.MagicMock()

    # Call the function with mocked dependencies
    result = process_message("example_debts_id", s3_client=mock_s3, logger=mock_logger)

    # Assert that the correct result is returned
    assert result == [["Kathy", "Patrick", "3359.0"], ["Kathy", "Ricky", "2746.0"]]

    # Assert that the logger was called with the correct message
    mock_logger.info.assert_called_once_with(
        "Debts simplified: [['Kathy', 'Patrick', '3359.0'], ['Kathy', 'Ricky', '2746.0']]"
    )


def test_process_message_error(mocker):
    # Mocking the S3 client to raise an exception
    mock_s3 = mocker.MagicMock()
    mock_s3.get_object.side_effect = Exception("S3 Error")

    # Mocking the logger
    mock_logger = mocker.MagicMock()

    # Call the function with mocked dependencies
    result = process_message("example_debts_id", s3_client=mock_s3, logger=mock_logger)

    # Assert that an empty list is returned
    assert result == []

    # Assert that the logger was called with the correct error message
    mock_logger.error.assert_called_once_with("Error processing message: S3 Error")


def test_save_results_to_s3_success(mocker):
    # Mocking the S3 client
    mock_s3 = mocker.MagicMock()

    # Mocking the logger
    mock_logger = mocker.MagicMock()

    # Call the function with mocked dependencies
    save_results_to_s3(
        [{"key": "value"}], "example_key", s3_client=mock_s3, logger=mock_logger
    )

    # Assert that the S3 client was called with the correct parameters
    mock_s3.put_object.assert_called_once_with(
        Bucket="example_bucket_name", Key="example_key", Body='[{"key": "value"}]'
    )

    # Assert that the logger was called with the correct message
    mock_logger.info.assert_called_once_with("Results saved to S3: example_key")


def test_save_results_to_s3_error(mocker):
    # Mocking the S3 client to raise an exception
    mock_s3 = mocker.MagicMock()
    mock_s3.put_object.side_effect = Exception("S3 Error")

    # Mocking the logger
    mock_logger = mocker.MagicMock()

    # Call the function with mocked dependencies
    save_results_to_s3(
        [{"key": "value"}], "example_key", s3_client=mock_s3, logger=mock_logger
    )

    # Assert that the logger was called with the correct error message
    mock_logger.error.assert_called_once_with("Error saving results to S3: S3 Error")
