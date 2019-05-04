class ParkingProvider():

    def provide(this, lat, lon):
        return {
            'summary': {
                'grade': 'good',
                'score': 50,
            },
            'data': None,
        }
