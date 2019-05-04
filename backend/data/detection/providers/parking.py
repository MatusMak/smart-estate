from data.models import Parking, Usage


class ParkingProvider():

    def provide(self, lat, lon):
        parking = self.get_nearest(lat, lon)
        usages = Usage.objects.filter(parking=parking)

        data = []
        for u in usages:
            data.append({
                'title': u.timeslot.name[0].upper()+u.timeslot.name[1:].lower(),
                'relative': int(round(100*(parking.capacity-u.full//u.weight)/parking.capacity, 0)),
                'absolute': parking.capacity-u.full//u.weight,
                'capacity': parking.capacity,
            })
        score = int(round(400*max((((parking.capacity-u.full//u.weight)/parking.capacity)**(1/6)-0.75), 0), 0))

        return {
            'summary': {
                'grade': self.scoreToGrade(score),
                'score': score,
            },
            'data': data,
        }

    def scoreToGrade(self, score):
        if score > 70:
            return 'good'
        elif score > 40:
            return 'okay'
        return 'bad'

    def get_nearest(self, lat, lon):
        parkings = Parking.objects.all()
        best = [
            parkings[0],
            (float(parkings[0].latitude) - lat)**2+(float(parkings[0].longitude) - lon)**2,
        ]

        for p in parkings[1:]:
            temp = [
                p,
                (float(p.latitude) - lat)**2+(float(p.longitude) - lon)**2,
            ]
            if temp[1] < best[1]:
                best = temp

        return best[0]
