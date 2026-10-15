class BaseMechanism:
    """Khung giao diện cơ sở: Bất kỳ cơ chế nào sinh ra chỉ cần kế thừa lớp này"""
    name = "base_mechanism"
    priority = 100

    def execute(self, context):
        """
        Nhận vào context (túi trạng thái chung của Microkernel)
        và tự do tính toán hoặc bổ sung dữ liệu vào context.
        """
        raise NotImplementedError
