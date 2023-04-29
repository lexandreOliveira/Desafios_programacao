# Reescreva o código apresentado, propondo melhorias. (Envie um print de seu código de preferência utilizando a extensão RayThis)

def next_video(id_aula_curso: str, slug_curso: str) -> str:
    """Recebe o ID de uma aula e seu respectivo curso e retorna a próxima aula
    
    Args:
        id_aula_curso: id de uma instancia da model aula curso
        slug_curso: slug de identificação do curso  (parte final de uma url)
        
    Returns:
    O ID da próxima aula
    """
    aula_curso = AulaCurso.objects.get(id=id_aula_curso)
    modulo = (
        Modulo.objects.prefetch_related('aulas')
        .filter(curso__slug_curso)
        .filter(aulas=aula_curso)
        .first()
    )
    
 







    aulas_modulo = modulo.aulas.all().order_by('-ordem')
    proxima_aula = None

    if aula_curso.ordem == aulas_modulo[0].ordem:
        proxima_aula = (
        Modulo.objects.filter(curso__slug=slug_curso)
        .get(ordem=(modulo.ordem + 1 ))
        .aulas.all()
        .filter()
        
        )
    
    else: 
        proxima_aula = aulas_modulo.get(ordem=aula_curso.ordem + 1 )
    
    return proxima_aula






# Reescrevendo o código 



from django.db.models import Prefetch

def next_video(id_aula_curso: str, slug_curso: str) -> str:
    """Utilizei o objeto Prefetch para otimizar o desempenho de consultas ao banco.
    Desta forma todas as instancias de AulaCurso são armazenadas no objeto Prefetch"""
    aula_curso = AulaCurso.objects.get(id=id_aula_curso)
    modulo = (
        Modulo.objects
        .filter(curso__slug_curso=slug_curso)
        .prefetch_related(
        Prefetch('aulas', queryset=AulasCurso.objects.all())
        )
        .get(aulas=aula_curso)
    )

    aulas_modulo = list(modulo.aulas.all().order_by('-ordem'))
    aula_curso_ind = aulas_modulo.index(aula_curso)     
    
    if aula_curso_ind == len(aulas_modulo) - 1:
        proximo_modulo = Modulo.objects.filter(
            curso__slug_curso=slug_curso,
            ordem=modulo.ordem + 1
        ).first()
        if proximo_modulo:
            proxima_aula = proximo_modulo.aulas.first()
        else:
            proxima_aula = None
    else:
        proxima_aula = aulas_modulo[aula_curso_ind + 1]

    if proxima_aula:
        return proxima_aula.id
    else:
        return None








