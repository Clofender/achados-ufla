from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Category, Item, Location, Profile
from occurrences.models import Occurrence


class Command(BaseCommand):
    help = "Cria um conjunto amplo de dados UFLA para demonstração local."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            help="Usuário existente que também receberá registros de demonstração.",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Remove apenas usuários demo e objetos associados antes de recriar os dados.",
        )

    def handle(self, *args, **options):
        user_model = get_user_model()
        demo_usernames = [
            "demo_aluno",
            "demo_aluno2",
            "demo_aluno3",
            "demo_aluno4",
            "demo_moderador",
            "demo_moderador2",
            "demo_admin",
        ]
        if options["username"]:
            demo_usernames.append(options["username"])

        if options["reset"]:
            demo_users = user_model.objects.filter(username__in=demo_usernames)
            reset_users = demo_users
            if options["username"]:
                reset_users = reset_users.exclude(username=options["username"])
            Item.objects.filter(owner__in=reset_users).delete()
            reset_users.delete()
            self.stdout.write("Dados demo anteriores removidos.")

        users = {}
        student_names = [
            ("demo_aluno", "Ana", "Silva"),
            ("demo_aluno2", "Bruno", "Souza"),
            ("demo_aluno3", "Camila", "Lima"),
            ("demo_aluno4", "Daniel", "Ferreira"),
        ]
        for index, (username, first_name, last_name) in enumerate(student_names, start=1):
            user, created = user_model.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": f"{username}@estudante.ufla.br",
                },
            )
            user.first_name = first_name
            user.last_name = last_name
            user.email = f"{username}@estudante.ufla.br"
            user.is_staff = False
            user.is_superuser = False
            user.set_password("Demo12345!")
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = Profile.Role.STUDENT
            profile.campus_id = f"2024{index:04d}"
            profile.phone = f"(35) 9912{index:04d}"
            profile.save()
            users[username] = user

        if options["username"]:
            extra_user = user_model.objects.get(username=options["username"])
            profile, _ = Profile.objects.get_or_create(user=extra_user)
            profile.role = Profile.Role.STUDENT
            profile.save()
            users[options["username"]] = extra_user

        moderators = []
        for index, username in enumerate(("demo_moderador", "demo_moderador2"), start=1):
            user, created = user_model.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": "Moderador",
                    "last_name": str(index),
                    "email": f"{username}@ufla.br",
                },
            )
            user.first_name = "Moderador"
            user.last_name = str(index)
            user.email = f"{username}@ufla.br"
            user.is_staff = True
            user.is_superuser = False
            user.set_password("Demo12345!")
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = Profile.Role.MODERATOR
            profile.save()
            permissions = Permission.objects.filter(
                content_type__app_label__in={"core", "occurrences"},
                codename__in={
                    "view_category", "add_category", "change_category", "delete_category",
                    "view_location", "add_location", "change_location", "delete_location",
                    "view_item", "add_item", "change_item", "delete_item",
                    "view_occurrence", "add_occurrence", "change_occurrence", "delete_occurrence",
                },
            )
            user.user_permissions.set(permissions)
            moderators.append(user)
        users["demo_moderador"] = moderators[0]
        users["demo_moderador2"] = moderators[1]

        administrator, _ = user_model.objects.get_or_create(
            username="demo_admin",
            defaults={
                "first_name": "Administrador",
                "last_name": "UFLA",
                "email": "demo_admin@ufla.br",
            },
        )
        administrator.first_name = "Administrador"
        administrator.last_name = "UFLA"
        administrator.email = "demo_admin@ufla.br"
        administrator.is_staff = True
        administrator.is_superuser = True
        administrator.set_password("Demo12345!")
        administrator.save()
        profile, _ = Profile.objects.get_or_create(user=administrator)
        profile.role = Profile.Role.ADMIN
        profile.save()
        users["demo_admin"] = administrator

        category_data = [
            ("Eletrônicos", "Celulares, notebooks, carregadores e acessórios."),
            ("Documentos", "Carteiras estudantis, documentos e identificações."),
            ("Chaves", "Chaves pessoais, chaveiros e controles."),
            ("Material acadêmico", "Livros, cadernos, calculadoras e apostilas."),
            ("Roupas e acessórios", "Jaquetas, bonés, mochilas e bolsas."),
            ("Óculos e relógios", "Óculos, relógios e acessórios pessoais."),
            ("Equipamentos esportivos", "Garrafas, bolas e equipamentos esportivos."),
            ("Instrumentos musicais", "Instrumentos e acessórios para estudo musical."),
            ("Áudio e fotografia", "Fones, câmeras e acessórios fotográficos."),
            ("Outros", "Objetos que não se encaixam nas categorias anteriores."),
        ]
        categories = {}
        for name, description in category_data:
            category, _ = Category.objects.get_or_create(
                name=name,
                defaults={"description": description, "is_active": True},
            )
            category.description = description
            category.is_active = True
            category.save()
            categories[name] = category

        location_data = [
            ("Biblioteca Universitária", "Prédio central da Biblioteca UFLA."),
            ("Restaurante Universitário", "Área de atendimento e mesas do RU."),
            ("Prédio DEX", "Departamento de Ciências Exatas."),
            ("Prédio DCC", "Departamento de Ciência da Computação."),
            ("Centro de Convivência", "Área de alimentação e convivência estudantil."),
            ("Ginásio Poliesportivo", "Ginásio e arquibancadas."),
            ("Auditório", "Auditórios e salas destinadas a eventos."),
            ("Prédio Administrativo", "Secretarias e setores administrativos."),
            ("Estacionamento Central", "Estacionamento próximo ao campus central."),
            ("Bosque", "Área arborizada do campus."),
            ("Laboratório de Química", "Setor de laboratórios do DQI."),
            ("Laboratório de Física", "Setor de laboratórios do DFI."),
            ("Estação de Ônibus", "Ponto de embarque e desembarque."),
            ("Praça Cota Zero", "Área de circulação no campus central."),
        ]
        locations = {}
        for name, description in location_data:
            location, _ = Location.objects.get_or_create(
                name=name,
                defaults={"description": description},
            )
            location.description = description
            location.save()
            locations[name] = location

        item_specs = [
            ("Celular preto com capa azul", "Encontrado em uma mesa próxima à entrada.", "Capa azul, riscos discretos e fone conectado.", "FOUND", "Eletrônicos", "Biblioteca Universitária"),
            ("Notebook prata", "Noticiário encontrado na sala de estudos.", "Adesivo azul na tampa e carregador branco.", "LOST", "Eletrônicos", "Prédio DCC"),
            ("Carregador para celular", "Tomada próxima ao corredor.", "Cabo USB-C, marca apagada e comprimento longo.", "FOUND", "Eletrônicos", "Centro de Convivência"),
            ("Fone sem fio branco", "Encontrado perto da bancada.", "Estojo aberto e sem identificador externo.", "FOUND", "Áudio e fotografia", "Prédio DEX"),
            ("Mochila preta", "Abandonada próxima ao bicicletário.", "Cinto vermelho e bolso lateral resistente.", "FOUND", "Roupas e acessórios", "Ginásio Poliesportivo"),
            ("Mochila vermelha", "Devolvida ao estudante após confirmação.", "Chaveiro de folha no zíper.", "RETURNED", "Roupas e acessórios", "Estação de Ônibus"),
            ("Carteira estudantil", "Identificação encontrada em uma carteira.", "Foto visível e validade 2026.", "FOUND", "Documentos", "Restaurante Universitário"),
            ("Cartão de transporte", "Cartão encontrado no balcão.", "Capa transparente com adesivo verde.", "LOST", "Documentos", "Estação de Ônibus"),
            ("RG em capa azul", "Documento entregue na recepção.", "Capa azul com nome parcialmente visível.", "FOUND", "Documentos", "Prédio Administrativo"),
            ("Chave com quatro argolas", "Chaves deixadas em banco externo.", "Quatro chaves e chaveiro da UFLA.", "FOUND", "Chaves", "Bosque"),
            ("Chave de residência", "Encontrada próxima ao estacionamento.", "Uma chave comum e chaveiro metálico.", "LOST", "Chaves", "Estacionamento Central"),
            ("Controle remoto pequeno", "Encontrado sob uma cadeira.", "Controle preto com tampa no compartimento.", "ARCHIVED", "Eletrônicos", "Auditório"),
            ("Calculadora científica", "Deixada sobre uma carteira.", "Modelo com tampa protetora.", "FOUND", "Material acadêmico", "Prédio DEX"),
            ("Caderno de cálculo", "Caderno esquecido na sala.", "Capa preta e nome no início.", "LOST", "Material acadêmico", "Prédio DEX"),
            ("Livro de Engenharia", "Livro encontrado na mesa de devolução.", "Marcações a lápis no índice.", "FOUND", "Material acadêmico", "Biblioteca Universitária"),
            ("Apostila de anatomia", "Pacote de folhas separado.", "Muitas páginas grampeadas e capa verde.", "LOST", "Material acadêmico", "Laboratório de Química"),
            ("Jaqueta azul", "Jaqueta encontrada no bloco de estudos.", "Capuz removível e bolso direito rasgado.", "FOUND", "Roupas e acessórios", "Centro de Convivência"),
            ("Boné cinza", "Boné esquecido em arquibancada.", "Logo bordado em branco.", "FOUND", "Roupas e acessórios", "Ginásio Poliesportivo"),
            ("Guarda-chuva preto", "Encontrado encostado em parede.", "Cabo de madeira sintética.", "LOST", "Outros", "Praça Cota Zero"),
            ("Óculos de grau", "Óculos encontrados dentro de estojo.", "Armação marrom e lente com risco leve.", "FOUND", "Óculos e relógios", "Biblioteca Universitária"),
            ("Relógio esportivo", "Encontrado próximo à pista.", "Pulseira preta e pulseira extra na caixa.", "FOUND", "Óculos e relógios", "Ginásio Poliesportivo"),
            ("Garrafa térmica verde", "Garrafa encontrada ao lado de mesa.", "Marca de adesivo com nome parcialmente apagado.", "FOUND", "Equipamentos esportivos", "Ginásio Poliesportivo"),
            ("Bola de vôlei", "Bola entregue após treino.", "Marca visível e pequena sujeira.", "ARCHIVED", "Equipamentos esportivos", "Ginásio Poliesportivo"),
            ("Violão infantil", "Instrumento encontrado no auditório.", "Cordas novas e capa vermelha.", "LOST", "Instrumentos musicais", "Auditório"),
            ("Capa para teclado", "Capa longa deixada no palco.", "Tecido preto e etiqueta interna.", "FOUND", "Instrumentos musicais", "Auditório"),
            ("Câmera compacta", "Câmera entregue ao setor.", "Lente limpa e cartão de memória removido.", "FOUND", "Áudio e fotografia", "Bosque"),
            ("Tripé leve", "Tripé abandonado próximo ao estacionamento.", "Cor preta e bolsa de transporte.", "LOST", "Áudio e fotografia", "Estacionamento Central"),
            ("Pen drive azul", "Encontrado em computador da biblioteca.", "Capacidade de 64 GB e chaveiro pequeno.", "FOUND", "Eletrônicos", "Biblioteca Universitária"),
            ("Mouse sem fio", "Mouse esquecido em laboratório.", "Cor cinza e receptor USB separado.", "FOUND", "Eletrônicos", "Laboratório de Química"),
            ("Extensão elétrica", "Fio encontrado no laboratório.", "Comprimento curto e adaptador triplo.", "ARCHIVED", "Eletrônicos", "Laboratório de Física"),
            ("Casaco de frio", "Peça encontrada em sala vazia.", "Forro cinza e bolso interno.", "LOST", "Roupas e acessórios", "Prédio DCC"),
            ("Crachá de visitante", "Credencial encontrada na entrada.", "Nome ilegível e cordão verde.", "FOUND", "Documentos", "Prédio Administrativo"),
            ("Garfo e talheres", "Talheres encontrados em bandeja.", "Estojo simples de tecido.", "ARCHIVED", "Outros", "Restaurante Universitário"),
            ("Pulseira esportiva", "Pulseira encontrada na pista.", "Silicone preto e pequeno defeito.", "FOUND", "Óculos e relógios", "Ginásio Poliesportivo"),
            ("Óculos de sol", "Óculos encontrados em mesa externa.", "Armação preta e estojo azul.", "LOST", "Óculos e relógios", "Praça Cota Zero"),
            ("Caixa de som portátil", "Equipamento deixado no auditório.", "Conexão Bluetooth e cabo USB.", "FOUND", "Áudio e fotografia", "Auditório"),
            ("Kit de desenho", "Estojo completo esquecido.", "Inclui lápis, borracha e compasso.", "FOUND", "Material acadêmico", "Prédio DEX"),
            ("Chaveiro com nome", "Chaveiro encontrado no corredor.", "Nome gravado em placa metálica.", "LOST", "Chaves", "Centro de Convivência"),
            ("Capa de notebook", "Capa encontrada no pátio.", "Vermelha e com compartimento externo.", "FOUND", "Eletrônicos", "Praça Cota Zero"),
        ]

        now = timezone.now()
        student_users = [users[name] for name in ("demo_aluno", "demo_aluno2", "demo_aluno3", "demo_aluno4")]
        created_items = {}
        for index, spec in enumerate(item_specs):
            title, description, characteristics, status_name, category_name, location_name = spec
            owner = student_users[index % len(student_users)]
            status = getattr(Item.Status, status_name)
            approved = status in {Item.Status.FOUND, Item.Status.LOST, Item.Status.RETURNED}
            item, _ = Item.objects.update_or_create(
                title=title,
                defaults={
                    "description": description,
                    "characteristics": characteristics,
                    "status": status,
                    "category": categories[category_name],
                    "location": locations[location_name],
                    "owner": owner,
                    "is_public": status != Item.Status.ARCHIVED,
                    "approved": approved,
                    "approved_by": moderators[index % len(moderators)] if approved else None,
                    "approved_at": now - timedelta(days=(index % 18)) if approved else None,
                },
            )
            created_items[title] = item

        occurrence_specs = [
            ("Celular preto com capa azul", "FINDING", "PENDING", "Biblioteca Universitária", "Celular entregue na recepção; aguarda identificação."),
            ("Celular preto com capa azul", "RETURN_REQUEST", "APPROVED", "Biblioteca Universitária", "Identidade confirmada pela comanda acadêmica."),
            ("Carteira estudantil", "FINDING", "COMPLETED", "Restaurante Universitário", "Documento entregue ao setor responsável."),
            ("Notebook prata", "LOSS", "PENDING", "Prédio DCC", "Estudante perdeu o notebook após aula."),
            ("Caderno de cálculo", "LOSS", "APPROVED", "Prédio DEX", "Caderno localizado com marcações próprias."),
            ("Caderno de cálculo", "RETURN_REQUEST", "COMPLETED", "Prédio DEX", "Entregue ao estudante após validação."),
            ("Óculos de grau", "FINDING", "PENDING", "Biblioteca Universitária", "Estojo encontrado em mesa reservada."),
            ("Óculos de sol", "LOSS", "REJECTED", "Praça Cota Zero", "Não foi possível confirmar a identificação."),
            ("Chave com quatro argolas", "FINDING", "PENDING", "Bosque", "Chaves entregues ao posto interno."),
            ("Chave de residência", "LOSS", "APPROVED", "Estacionamento Central", "Chaves encontradas próximas ao local informado."),
            ("Câmera compacta", "FINDING", "COMPLETED", "Bosque", "Câmera devolvida ao proprietário."),
            ("Garrafa térmica verde", "FINDING", "PENDING", "Ginásio Poliesportivo", "Garrafa encontrada após competição."),
            ("Boné cinza", "FINDING", "APPROVED", "Ginásio Poliesportivo", "Boné localizado na arquibancada."),
            ("Jaqueta azul", "FINDING", "REJECTED", "Centro de Convivência", "Descrição não corresponde ao objeto."),
            ("Relógio esportivo", "FINDING", "PENDING", "Ginásio Poliesportivo", "Relógio entregue na secretaria do ginásio."),
            ("Violão infantil", "LOSS", "PENDING", "Auditório", "Instrumento perdido após ensaio."),
            ("Pen drive azul", "FINDING", "COMPLETED", "Biblioteca Universitária", "Entregue após verificação do conteúdo."),
            ("Mouse sem fio", "FINDING", "APPROVED", "Laboratório de Química", "Mouse separado de outros equipamentos."),
            ("Calculadora científica", "FINDING", "PENDING", "Prédio DEX", "Calculadora aguardando identificação."),
            ("Livro de Engenharia", "FINDING", "APPROVED", "Biblioteca Universitária", "Livro localizado no balcão de devolução."),
            ("Crachá de visitante", "FINDING", "COMPLETED", "Prédio Administrativo", "Crachá devolvido ao setor."),
            ("Mochila vermelha", "RETURN_REQUEST", "APPROVED", "Estação de Ônibus", "Identidade confirmada e mochila entregue."),
        ]

        for index, spec in enumerate(occurrence_specs):
            item_title, occurrence_type_name, status_name, location_name, notes = spec
            item = created_items[item_title]
            reporter = student_users[index % len(student_users)]
            moderator = moderators[index % len(moderators)]
            occurrence_type = getattr(Occurrence.Type, occurrence_type_name)
            status = getattr(Occurrence.Status, status_name)
            seed_anchor = now.replace(minute=0, second=0, microsecond=0)
            occurred_at = seed_anchor - timedelta(days=(index % 45), hours=(index % 6))
            reviewed = status != Occurrence.Status.PENDING
            occurrence, _ = Occurrence.objects.update_or_create(
                item=item,
                occurrence_type=occurrence_type,
                reporter=reporter,
                defaults={
                    "occurred_at": occurred_at,
                    "location": locations[location_name],
                    "notes": notes,
                    "status": status,
                    "reviewed_by": moderator if reviewed else None,
                    "reviewed_at": occurred_at + timedelta(hours=5) if reviewed else None,
                    "returned_to": reporter if status in {Occurrence.Status.APPROVED, Occurrence.Status.COMPLETED} else None,
                    "return_notes": "Entrega validada pela equipe UFLA." if status == Occurrence.Status.COMPLETED else "",
                },
            )

        counts = {
            "users": user_model.objects.filter(username__in=demo_usernames).count(),
            "categories": Category.objects.count(),
            "locations": Location.objects.count(),
            "items": Item.objects.filter(owner__in=[u for u in users.values() if u]).count(),
            "occurrences": Occurrence.objects.filter(reporter__in=student_users).count(),
        }
        self.stdout.write(
            self.style.SUCCESS(
                "Dados UFLA criados: "
                f"{counts['users']} usuários, {counts['categories']} categorias, "
                f"{counts['locations']} locais, {counts['items']} objetos e "
                f"{counts['occurrences']} ocorrências."
            )
        )
