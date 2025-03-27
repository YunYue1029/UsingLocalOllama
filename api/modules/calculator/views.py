from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def calculate(request):
    try:
        num1 = float(request.data.get('num1'))
        num2 = float(request.data.get('num2'))
        operation = request.data.get('operation')
        
        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                return Response(
                    {"error": "Cannot divide by zero"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            result = num1 / num2
        else:
            return Response(
                {"error": "Invalid operation. Use +, -, *, or /"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response({
            "num1": num1,
            "num2": num2,
            "operation": operation,
            "result": result
        }, status=status.HTTP_200_OK)
        
    except (TypeError, ValueError):
        return Response(
            {"error": "Please provide valid numbers"},
            status=status.HTTP_400_BAD_REQUEST
        )
