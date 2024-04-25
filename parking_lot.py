import json
import boto3
import random
import string

# python3.12

class Car:
    def __init__(self, license_plate):
        self.license_plate = license_plate

    # magicmethod
    def __str__(self):
        return self.license_plate

    def park(self, parking_lot_array, spot):
        parking_lot_array[spot] = "assigned"
        print(f"Car with license plate {self.license_plate} parked successfully in spot {spot}.")

class ParkingLot:
    def __init__(self, parking_lot_size, spot_length=8, spot_width=12):
        self.size = parking_lot_size
        self.spot_area = spot_length * spot_width
        self.num_spots = parking_lot_size // self.spot_area
        print("Num of spots", self.num_spots)
        self.lot_array = ['unassigned'] * self.num_spots
        self.mapping = {}

    def park_car(self, car):
        if 'unassigned' in self.lot_array:
            spot = random.choice([i for i, val in enumerate(self.lot_array) if val == 'unassigned'])
            car.park(self.lot_array, spot)
            self.mapping[spot] = str(car)
        else:
            print("Parking lot is full. Exiting the program.")
            # Optional/Bonus: Save parking lot state to a JSON object
            self.save_to_json()
            self.upload_to_s3("your_bucket_name", "parking_lot_mapping.json")
            exit()

    def save_to_json(self):
        print("----json-obj----::", self.mapping)
        with open('parking_lot_mapping.json', 'w') as f:
            json.dump(self.mapping, f)

    def upload_to_s3(self, bucket_name, file_name):
        print("uploading to s3......")
        s3_client = boto3.client(
            's3',
            aws_access_key_id='s3_aws_access_key_id',
            aws_secret_access_key='s3_aws_secret_access_key'
        )
        with open(file_name, "rb") as f:
            s3_client.put_object(Body=f, Bucket=bucket_name, Key=file_name)


def main(cars):
    parking_lot_size = 2000  # Example parking lot size
    parking_lot = ParkingLot(parking_lot_size)

    for car in cars:
        parking_lot.park_car(car)

    print("All cars parked successfully.")

    # Optional/Bonus: Upload parking lot mapping to S3 bucket
    parking_lot.save_to_json()
    parking_lot.upload_to_s3("your_bucket_name", "parking_lot_mapping.json")


if __name__ == "__main__":
    cars = [Car(''.join(random.choices(string.ascii_uppercase + string.digits, k=7))) for _ in
            range(30)]  # Generating random license plates for 30 cars
    # main(cars)

    parking_lot_size = 2000  # Example parking lot size
    parking_lot = ParkingLot(parking_lot_size)

    for car in cars:
        parking_lot.park_car(car)

    print("All cars parked successfully.")

    # Optional/Bonus: Upload parking lot mapping to S3 bucket
    parking_lot.save_to_json()
    parking_lot.upload_to_s3("your_bucket_name", "parking_lot_mapping.json")

