import json
import csv
import pickle
import os
from datetime import datetime

class PatientRecord:
    
    def __init__(self, patient_id: str, name: str, birth_year: int, gender: str, height: float, weight: float):
        self.patient_id = patient_id
        self.name = name
        self.birth_year = birth_year
        self.gender = gender
        self.height = height  # 단위: cm
        self.weight = weight  # 단위: kg
        self.bmi, self.obesity_status = self._calculate_bmi_and_obesity()

    def _calculate_bmi_and_obesity(self):
        if self.height <= 0:
            return 0.0, "측정 불가"
        
        height_m = self.height / 100.0
        bmi = round(self.weight / (height_m ** 2), 2)
        
        if bmi < 18.5:
            status = "저체중"
        elif 18.5 <= bmi < 23:
            status = "정상"
        elif 23 <= bmi < 25:
            status = "과체중"
        elif 25 <= bmi < 30:
            status = "경도비만"
        else:
            status = "중등도비만 이상"
            
        return bmi, status

    def to_dict(self) -> dict:
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "weight": self.weight,
            "bmi": self.bmi,
            "obesity_status": self.obesity_status
        }


class PatientManager:
    def __init__(self):
        self.records = {}  # {patient_id: PatientRecord 객체}

    def generate_id(self) -> str:
        current_year = datetime.now().year
        prefix = f"P{current_year}"
        
        existing_nums = [
            int(pid.replace(prefix, "")) 
            for pid in self.records.keys() 
            if pid.startswith(prefix) and pid.replace(prefix, "").isdigit()
        ]
        next_seq = max(existing_nums, default=0) + 1
        return f"{prefix}{next_seq:03d}"

    def add_record(self, name: str, birth_year: int, gender: str, height: float, weight: float) -> PatientRecord:
        patient_id = self.generate_id()
        record = PatientRecord(patient_id, name, birth_year, gender, height, weight)
        self.records[patient_id] = record
        print(f"[추가 완료] 식별번호: {patient_id}, 이름: {name}")
        return record

    def save_to_file(self, filename: str, file_format: str = "json"):
        try:
            data_list = [rec.to_dict() for rec in self.records.values()]
            file_format = file_format.lower()

            if file_format == "json":
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(data_list, f, ensure_ascii=False, indent=4)
                    
            elif file_format == "csv":
                if not data_list:
                    print("[알림] 저장할 데이터가 없습니다.")
                    return
                fieldnames = list(data_list[0].keys())
                with open(filename, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data_list)
                    
            elif file_format == "txt":
                with open(filename, "w", encoding="utf-8") as f:
                    for rec in self.records.values():
                        line = f"ID: {rec.patient_id} | 이름: {rec.name} | 생년: {rec.birth_year} | 성별: {rec.gender} | 키: {rec.height}cm | 체중: {rec.weight}kg | BMI: {rec.bmi} | 비만도: {rec.obesity_status}\n"
                        f.write(line)
                        
            elif file_format == "pickle":
                with open(filename, "wb") as f:
                    pickle.dump(self.records, f)
            else:
                raise ValueError(f"지원하지 않는 파일 포맷입니다: {file_format}")
                
            print(f"[성공] 파일 저장 완료: {filename} (포맷: {file_format})")
            
        except Exception as e:
            print(f"[저장 오류 발생] {e}")

    def load_from_file(self, filename: str, file_format: str = "json"):
        try:
            if not os.path.exists(filename):
                raise FileNotFoundError(f"지정한 경로에 파일이 존재하지 않습니다: {filename}")

            file_format = file_format.lower()

            if file_format == "json":
                with open(filename, "r", encoding="utf-8") as f:
                    data_list = json.load(f)
                    self.records = {}
                    for item in data_list:
                        rec = PatientRecord(
                            item["patient_id"], item["name"], item["birth_year"],
                            item["gender"], item["height"], item["weight"]
                        )
                        self.records[item["patient_id"]] = rec
                        
            elif file_format == "csv":
                self.records = {}
                with open(filename, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        rec = PatientRecord(
                            row["patient_id"], row["name"], int(row["birth_year"]),
                            row["gender"], float(row["height"]), float(row["weight"])
                        )
                        self.records[row["patient_id"]] = rec
                        
            elif file_format == "pickle":
                with open(filename, "rb") as f:
                    self.records = pickle.load(f)
                    
            elif file_format == "txt":
                raise NotImplementedError("TXT 파일은 읽기 전용이므로 객체 복원 로드가 지원되지 않습니다. JSON 또는 Pickle을 사용해주세요.")
            else:
                raise ValueError(f"지원하지 않는 파일 포맷입니다: {file_format}")
                
            print(f"[성공] 파일 로드 완료: {filename} (총 {len(self.records)}건)")

        except FileNotFoundError as fnf_error:
            print(f"[예외 처리 - 파일 부재]: {fnf_error}")
        except (json.JSONDecodeError, pickle.UnpicklingError) as parse_error:
            print(f"[예외 처리 - 파일 손상]: 파일 포맷이 손상되었거나 형식이 올바르지 않습니다. ({parse_error})")
        except Exception as e:
            print(f"[예외 처리 - 예상치 못한 오류]: {e}")