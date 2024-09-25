from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.cores.models import AcademicLevel, GroupStudent, TypeInvestigation
from apps.prototypes.models import Member, Prototype, TeacherRoles
from apps.school.models import Student, Teacher
from apps.users.serializers import UserListSerializer

User = get_user_model()


def get_teacher_advisors(obj, rol, is_name=True):
    try:
        queryset_teachers = Prototype.objects.get(id=obj.id).teacher_advisors.all() 
        for teacher in queryset_teachers:
        
            
                if teacher.roles == rol:
                    if is_name:
                        try:
                            user = Teacher.objects.get(id=teacher.teacher_data_id).user
                            serializer = UserListSerializer(user)
                            user = serializer.data
                            return f"{user['first_name']} {user['last_name']}"

                        except KeyError:
                            return None
                        
                    return teacher
        
        
    except (Prototype.DoesNotExist, Teacher.DoesNotExist):  
        return None

class StudentListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(default=None) 
    specialty = serializers.CharField(source="get_specialty_display", default=None, read_only=True)
    group = serializers.SerializerMethodField(default=None, read_only=True)

    def get_group(self, obj):
        try:
            return GroupStudent.objects.get(id=obj.group_id).text
        except GroupStudent.DoesNotExist:
            return None
        

    class Meta:
        model = Student
        fields = [
            "id",
            "group",
            "specialty",
            "user",
            # "turn",
            "created",
            "school_control_number",
        ]

class StudentRetrieveSerializer(serializers.ModelSerializer):
    user = UserListSerializer(default=None)
    class Meta:
        model = Student
        fields = [
            "id",
            "group",
            "specialty",
            "user",
            # "turn",
            "school_control_number",
        ]


class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "group",
            "specialty",
            "user",
            # "turn",
            "school_control_number",
        ]


class MemberListSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField(default=None, read_only=True)

    def get_student(self, *args, **kwargs):
        try:
            student = Student.objects.get(student=kwargs.get('student'))
            return student.__dict__
        except Student.DoesNotExist:
            return None
        
    class Meta:
        model = Member
        fields = [
            "id",
            "student",
            "author",
        ]


class MemberCreatetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            "id",
            "student",
            "author",
        ]


class TeacherListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(
        read_only=True, 
        default=None
    )
    academic_level = serializers.SerializerMethodField(
        read_only=True, 
        default=None
    )
    
    
    def get_academic_level(self, obj):
        try:
            return AcademicLevel.objects.get(id=obj.academic_level_id).text
        except AcademicLevel.DoesNotExist:
            return None
    
    
    class Meta:
        model = Teacher
        fields = ["id", "budget_code", "academic_level", "user", "created"]


class TeacherRetrieveSerializer(serializers.ModelSerializer):
    user = UserListSerializer(
        read_only=True, 
        default=None
    )
    class Meta:
        model = Teacher
        fields = ["id", "budget_code", "academic_level", "user"]


class TeacherCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ["id", "budget_code", "academic_level", "user"]


class TeacherRolesListSerializer(serializers.ModelSerializer):
    teacher_data = TeacherListSerializer(default=None)

    class Meta:
        model = TeacherRoles
        fields = ["id", "teacher_data", "roles"]


class TeacherRolesCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherRoles
        fields = ["teacher_data", "roles"]


def get_student(author, prototype_id, is_user_data=False):
        try:
            member = Prototype.objects.get(id=prototype_id).members.get(author=author)
            student = Student.objects.get(id=member.student_id)
            if is_user_data:
                return student.user
            return student
        except Member.DoesNotExist:
            return None 

class PrototypeListSerializer(serializers.ModelSerializer):
    modality = serializers.CharField(source="get_modality_display", read_only=True)
    type_investigation = serializers.SerializerMethodField(read_only=True, default=None)
    members = serializers.SerializerMethodField(read_only=True, default=[])
    methodological_advisor = serializers.SerializerMethodField(read_only=True, default=None)
    teacher_methods = serializers.SerializerMethodField(read_only=True, default=None)
    technical_advisor = serializers.SerializerMethodField(read_only=True, default=None)

    def get_type_investigation(self, obj):
        try:
            return TypeInvestigation.objects.get(id=obj.type_investigation_id).text
        except TypeInvestigation.DoesNotExist:
            return None 
        
    def get_members(self, obj):
        students = []
        queryset_members = Prototype.objects.get(id=obj.id).members.all() # type: ignore
        
        for member in queryset_members:
            try:
                student = Student.objects.get(id=member.student_id).__dict__
                user_data = User.objects.get(id=student["user_id"])
            except User.DoesNotExist:
                user_data = None
             
            students.append(
                    {
                        "id": member.id,
                        "name":f"{user_data.first_name} {user_data.last_name}" # type: ignore
                    }
                )

        return students
    
    
    def get_methodological_advisor(self, obj):
        return get_teacher_advisors(obj, "AM")

        
    def get_technical_advisor(self, obj):
            return get_teacher_advisors(obj, "AT")
   
        
    def get_teacher_methods(self, obj):
        return get_teacher_advisors(obj, "AM")
    
    class Meta:
        model = Prototype
        fields = [
            "id",
            "name",
            "registry_number",
            "modality",
            "type_investigation",
            "qualification",
            "members",
            "teacher_methods",
            "methodological_advisor",
            "technical_advisor",
            "created"
        ]


class PrototypeRetrieveSerializer(serializers.ModelSerializer):
     class Meta:
        model = Prototype
        fields = [
            "id",
            "name",
            "registry_number",
            "modality",
            "type_investigation",
            "qualification",
            "members",
            "teacher_methods",
            "teacher_advisors",
            "created"
        ]

class PrototypeCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prototype
        fields = [
            "name",
            "registry_number",
            "modality",
            "type_investigation",
            "qualification",
            "members",
            "teacher_methods",
            "teacher_advisors",
        ]

class PrototypeDownloadSerializers(serializers.ModelSerializer):
    modality = serializers.CharField(source="get_modality_display", read_only=True)
    type_investigation = serializers.SerializerMethodField(read_only=True, default=None)
    teacher_methods = serializers.SerializerMethodField(read_only=True, default=None)

    # Srializer methodological advisor
    methodological_advisor = serializers.SerializerMethodField(read_only=True, default=None)
    budget_code_m = serializers.SerializerMethodField(read_only=True, default=None)
    academic_level_m = serializers.SerializerMethodField(read_only=True, default=None)
    email_m = serializers.SerializerMethodField(read_only=True, default=None)
    address_m = serializers.SerializerMethodField(read_only=True, default=None)
    phone_m = serializers.SerializerMethodField(read_only=True, default=None)

    # Serializer tecnical advisor
    technical_advisor = serializers.SerializerMethodField(read_only=True, default=None)
    budget_code_t = serializers.SerializerMethodField(read_only=True, default=None)
    academic_level_t = serializers.SerializerMethodField(read_only=True, default=None)
    email_t = serializers.SerializerMethodField(read_only=True, default=None)
    address_t = serializers.SerializerMethodField(read_only=True, default=None)
    phone_t = serializers.SerializerMethodField(read_only=True, default=None)

    # Serializer Members
    author_1 = serializers.IntegerField(default=1)
    member_1 = serializers.SerializerMethodField(read_only=True, default=None)
    group_1 = serializers.SerializerMethodField(read_only=True, default=None)
    speciality_1 = serializers.SerializerMethodField(read_only=True, default=None)
    control_number_1 = serializers.SerializerMethodField(read_only=True, default=None)
    email_1 = serializers.SerializerMethodField(read_only=True, default=None)
    address_1 = serializers.SerializerMethodField(read_only=True, default=None)
    phone_1 = serializers.SerializerMethodField(read_only=True, default=None)

    author_2 = serializers.IntegerField(default=2)
    member_2 = serializers.SerializerMethodField(read_only=True, default=None)
    group_2 = serializers.SerializerMethodField(read_only=True, default=None)
    speciality_2 = serializers.SerializerMethodField(read_only=True, default=None)
    control_number_2 = serializers.SerializerMethodField(read_only=True, default=None)
    email_2 = serializers.SerializerMethodField(read_only=True, default=None)
    address_2 = serializers.SerializerMethodField(read_only=True, default=None)
    phone_2 = serializers.SerializerMethodField(read_only=True, default=None)

    author_3 = serializers.IntegerField(default=3)
    member_3 = serializers.SerializerMethodField(read_only=True, default=None)
    group_3 = serializers.SerializerMethodField(read_only=True, default=None)
    speciality_3 = serializers.SerializerMethodField(read_only=True, default=None)
    control_number_3 = serializers.SerializerMethodField(read_only=True, default=None)
    email_3 = serializers.SerializerMethodField(read_only=True, default=None)
    address_3 = serializers.SerializerMethodField(read_only=True, default=None)
    phone_3 = serializers.SerializerMethodField(read_only=True, default=None)

    author_4 = serializers.IntegerField(default=4)
    member_4 = serializers.SerializerMethodField(read_only=True, default=None)
    group_4 = serializers.SerializerMethodField(read_only=True, default=None)
    speciality_4 = serializers.SerializerMethodField(read_only=True, default=None)
    control_number_4 = serializers.SerializerMethodField(read_only=True, default=None)
    email_4 = serializers.SerializerMethodField(read_only=True, default=None)
    address_4 = serializers.SerializerMethodField(read_only=True, default=None)
    phone_4 = serializers.SerializerMethodField(read_only=True, default=None)
    

    def get_type_investigation(self, obj):
        try:
            return TypeInvestigation.objects.get(id=obj.type_investigation_id).text
        except TypeInvestigation.DoesNotExist:
            return None

    def get_teacher_methods(self, obj):
        try:
            teacher = Teacher.objects.get(id=obj.teacher_methods_id).user
            serializer = UserListSerializer(teacher)
            return f"{serializer.data['first_name']} {serializer.data['last_name']}" # type: ignore
        except Teacher.DoesNotExist:
            return None
 
    def get_methodological_advisor(self, obj):
            return get_teacher_advisors(obj, "AM")


    def get_budget_code_m(self, obj):
        methodological = get_teacher_advisors(obj, "AM", False)
        return Teacher.objects.get(id=methodological.teacher_data_id).budget_code # type: ignore
    
    def get_academic_level_m(self, obj):
        methodological = get_teacher_advisors(obj, "AM", False)
        teacher = Teacher.objects.get(id=methodological.teacher_data_id) # type: ignore
        return AcademicLevel.objects.get(id=teacher.academic_level_id).text # type: ignore
    
    def get_email_m(self, obj):
        return get_teacher_advisors(obj, "AM", False).get("email") # type: ignore
        
    def get_address_m(self, obj):
        return get_teacher_advisors(obj, "AM", False).get("address") # type: ignore
    
    def get_phone_m(self, obj):
        return get_teacher_advisors(obj, "AM", False).get("number_phone") # type: ignore
    
    def get_technical_advisor(self, obj):
        return get_teacher_advisors(obj, "AT", False).get("email") # type: ignore

    
    def get_budget_code_t(self, obj):
        methodological = get_teacher_advisors(obj, "AT", False)
        return Teacher.objects.get(id=methodological.teacher_data_id).budget_code # type: ignore
    
    def get_academic_level_t(self, obj):
        methodological = get_teacher_advisors(obj, "AT", False)
        teacher = Teacher.objects.get(id=methodological.teacher_data_id) # type: ignore
        return AcademicLevel.objects.get(id=teacher.academic_level_id).text # type: ignore
    
    def get_email_t(self, obj):
        return get_teacher_advisors(obj, "AT").get("email") # type: ignore   
    
    def get_address_t(self, obj):
        return get_teacher_advisors(obj, "AT").get("address") # type: ignore
    
    def get_phone_t(self, obj):
        return get_teacher_advisors(obj, "AT").get("number_phone") # type: ignore

    def get_member_1(self, obj):
        student = get_student(1, obj.id, True)
        if student is not None:
            return f"{student.first_name} {student.last_name}" # type: ignore
        
        return None 
    
    def get_group_1(self, obj):
        student = get_student(1, obj.id)
        if student is None:
            return student
        return student.group.text # type: ignore
    
    def get_speciality_1(self, obj):
        student = get_student(1, obj.id)
        if student is None:
            return student
        return student.specialty # type: ignore
    
    def get_control_number_1(self, obj):
        student = get_student(1, obj.id)
        if student is None:
            return student
        return student.school_control_number # type: ignore
    
    def get_email_1(self, obj):
        student = get_student(1, obj.id, True)
        if student is None:
            return student
        return student.email # type: ignore
    
    def get_address_1(self, obj):
        student = get_student(1, obj.id, True)
        if student is None:
            return student
        return student.address # type: ignore
    
    def get_phone_1(self, obj):
        student = get_student(1, obj.id, True)
        if student is None:
            return student
        return student.number_phone # type: ignore
    
    def get_member_2(self, obj):
        student = get_student(2, obj.id, True)
        if student is not None:
            return f"{student.first_name} {student.last_name}" # type: ignore
        
        return None 
    
    def get_group_2(self, obj):
        student = get_student(2, obj.id)
        if student is None:
            return student
        return student.group.text # type: ignore
    
    def get_speciality_2(self, obj):
        student = get_student(2, obj.id)
        if student is None:
            return student
        return student.specialty # type: ignore
    
    def get_control_number_2(self, obj):
        student = get_student(2, obj.id)
        if student is None:
            return student
        return student.school_control_number # type: ignore
    
    def get_email_2(self, obj):
        student = get_student(2, obj.id, True)
        if student is None:
            return student
        return student.email # type: ignore
    
    def get_address_2(self, obj):
        student = get_student(2, obj.id, True)
        if student is None:
            return student
        return student.address # type: ignore
    
    def get_phone_2(self, obj):
        student = get_student(2, obj.id, True)
        if student is None:
            return student
        return student.number_phone # type: ignore
    
    def get_member_3(self, obj):
        student = get_student(3, obj.id, True)
        if student is not None:
            return f"{student.first_name} {student.last_name}" # type: ignore
        
        return None 
    
    def get_group_3(self, obj):
        try:
            student = get_student(3, obj.id)
            return student.group.text # type: ignore
        except AttributeError:
            return None
        
    def get_speciality_3(self, obj):
        student = get_student(3, obj.id)
        if student is None:
            return student
        return student.specialty # type: ignore
    
    def get_control_number_3(self, obj):
        student = get_student(3, obj.id)
        if student is None:
            return student
        return student.school_control_number # type: ignore
    
    def get_email_3(self, obj):
        student = get_student(3, obj.id, True)
        if student is None:
            return student
        return student.email # type: ignore
    
    def get_address_3(self, obj):
        student = get_student(3, obj.id, True)
        if student is None:
            return student
        return student.address # type: ignore
    
    def get_phone_3(self, obj):
        student = get_student(3, obj.id, True)
        if student is None:
            return student
        return student.number_phone # type: ignore
    
    def get_member_4(self, obj):
        student = get_student(4, obj.id, True)
        if student is not None:
            return f"{student.first_name} {student.last_name}" # type: ignore
        
        return None 
    
    def get_group_4(self, obj):
        student = get_student(4, obj.id)
        if student is None:
            return student
        return student.group.text # type: ignore
         
    def get_speciality_4(self, obj):
        student = get_student(4, obj.id)
        if student is None:
            return student
        return student.specialty # type: ignore
    
    def get_control_number_4(self, obj):
        student = get_student(4, obj.id)
        if student is None:
            return student
        return student.school_control_number # type: ignore
    
    def get_email_4(self, obj):
        student = get_student(4, obj.id, True)
        if student is None:
            return student
        return student.email # type: ignore
    
    def get_address_4(self, obj):
        student = get_student(4, obj.id, True)
        if student is None:
            return student
        return student.address # type: ignore
    
    def get_phone_4(self, obj):
        student = get_student(4, obj.id, True)
        if student is None:
            return student
        return student.number_phone # type: ignore
    
    
    
    pass
    class Meta:
        model = Prototype
        fields = [
            "name",
            "registry_number",
            "modality",
            "type_investigation",
            "qualification",
            "teacher_methods",
            "methodological_advisor",
            "budget_code_m",
            "academic_level_m",
            "email_m",
            "address_m",
            "phone_m",
            "technical_advisor",
            "budget_code_t",
            "academic_level_t",
            "email_t",
            "address_t",
            "phone_t",
            "author_1",
            "member_1",
            "group_1",
            "speciality_1",
            "control_number_1",
            "email_1",
            "address_1",
            "phone_1",
            "author_2",
            "member_2",
            "group_2",
            "speciality_2",
            "control_number_2",
            "email_2",
            "address_2",
            "phone_2",
            "author_3",
            "member_3",
            "group_3",
            "speciality_3",
            "control_number_3",
            "email_3",
            "address_3",
            "phone_3",
            "author_4",
            "member_4",
            "group_4",
            "speciality_4",
            "control_number_4",
            "email_4",
            "address_4",
            "phone_4",
        ]


class MetaBaseList:
    fields = ["id", "text"]


class AcademyLevelSerializer(serializers.ModelSerializer):
    class Meta(MetaBaseList):
        model = AcademicLevel


class TypeInvestigationSerializer(serializers.ModelSerializer):
    class Meta(MetaBaseList):
        model = TypeInvestigation


class GroupStudentSerializer(serializers.ModelSerializer):

    class Meta(MetaBaseList):
        model = GroupStudent
